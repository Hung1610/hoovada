#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
import json
from datetime import datetime

# third-party modules
import dateutil.parser
from flask import g
from flask_restx import marshal
from slugify import slugify
from sqlalchemy import desc, func, or_

# own modules
from app.constants import messages
from common.utils.types import UserRole
from common.db import db
from common.es import get_model
from common.cache import cache
from common.controllers.controller import Controller
from common.utils.response import paginated_result, send_error, send_result
from common.utils.util import strip_tags
from common.dramatiq_producers import update_seen_questions
from app.modules.q_a.question.question_dto import QuestionDto
from app.modules.q_a.question.bookmark.bookmark_controller import QuestionBookmarkController
from elasticsearch_dsl import Q

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

QuestionUserInvite = db.get_model('QuestionUserInvite')
User = db.get_model('User')
UserFollow = db.get_model('UserFollow')
UserFriend = db.get_model('UserFriend')
Topic = db.get_model('Topic')
TopicBookmark = db.get_model('TopicBookmark')
Reputation = db.get_model('Reputation')
Answer = db.get_model('Answer')
Question = db.get_model('Question')
QuestionProposal = db.get_model('QuestionProposal')
QuestionShare = db.get_model('QuestionShare')

ESQuestion = get_model("Question")
ESTopic = get_model("Topic")

class QuestionController(Controller):
    query_classname = 'Question'
    special_filtering_fields = ['from_date', 'to_date', 'title', 'topic_id', 'is_shared']
    allowed_ordering_fields = ['created_date', 'updated_date', 'upvote_count', 'comment_count', 'share_count', 'answers_count']
    
    def create(self, data):
        if not isinstance(data, dict):
            return send_error(message=messages.ERR_WRONG_DATA_FORMAT)
        
        if not 'title' in data or data['title'] == "":
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('title'))

        # Handling user
        current_user = g.current_user
        data['user_id'] = current_user.id

        # Handling question title
        data['title'] = data['title'].strip().capitalize()
        if not data['title'].endswith('?'):
            return send_error(message=messages.ERR_QUESTION_NOT_END_WITH_QUESION_MARK)


        # Check if question already exists
        question = Question.query.filter(Question.title == data['title']).first()
        if question is not None:
            return send_error(message=messages.ERR_ALREADY_EXISTS)   

        # default fixed_topic
        if 'fixed_topic_id' not in data:
            topic = Topic.query.filter(Topic.name == 'Những lĩnh vực khác', Topic.is_fixed == True).first()
            data['fixed_topic_id'] = topic.id

        question = self._parse_question(data=data, question=None)
        try:     
            
            question.created_date = datetime.utcnow()
            question.last_activity = datetime.utcnow()
            question.slug = slugify(question.title)
            db.session.add(question)
            db.session.flush()

            # index to ES server
            question_dsl = ESQuestion(_id=question.id, question=strip_tags(question.question), title=question.title, user_id=question.user_id, slug=question.slug, created_date=question.created_date, updated_date=question.created_date)
            question_dsl.save()

            db.session.commit()
            cache.clear_cache(Question.__class__.__name__)

            try:
                bookmark_controller = QuestionBookmarkController()
                bookmark_controller.create(question_id=question.id)
                update_seen_questions.send(question.id, current_user.id)
            except Exception as e:
                print(e.__str__())
                pass
            # response data
            result = question._asdict()
            return send_result(data=marshal(result, QuestionDto.model_question_create_update_response))
        
        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_CREATE_FAILED.format(e))


    def get(self, args):
        try:
            query = self.get_query_results(args)
            res, code = paginated_result(query)
            
            results = []
            for question in res.get('data'):
                result = question._asdict()
                result['user'] = question.user
                result['fixed_topic'] = question.fixed_topic
                result['topics'] = question.topics
                results.append(result)
            
            res['data'] = marshal(results, QuestionDto.model_question_response)
            return res, code

        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_GET_FAILED.format(e))


    def get_by_id(self, object_id):
        if object_id is None:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('id'))

        try:
            if object_id.isdigit():
                question = Question.query.filter_by(id=object_id).first()
            else:
                question = Question.query.filter_by(slug=object_id).first()
            
            if question is None:
                return send_error(message=messages.ERR_NOT_FOUND)

            current_user = g.current_user
            if question.is_private:
                if current_user:
                    if not current_user == question.user:
                        if not question.invited_users.contains(current_user):
                            return send_error(message='Question can be seen by invitations only!')
                else:
                    return send_error(message='Question can be seen by invitations only!') 

            result = question._asdict()
            result['user'] = question.user
            result['topics'] = question.topics
            result['fixed_topic'] = question.fixed_topic
            
            if current_user:
                update_seen_questions.send(question.id, current_user.id)

            return send_result(data=marshal(result, QuestionDto.model_question_response))
        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_GET_FAILED.format(e))



    def invite(self, object_id, data):
        try:
            if not 'emails_or_usernames' in data:
                return send_error(message=messages.ERR_PLEASE_PROVIDE.format('emails_or_usernames'))

            if object_id is None:
                return send_error(message=messages.ERR_PLEASE_PROVIDE.format('id'))
                
            if object_id.isdigit():
                question = Question.query.filter_by(id=object_id).first()
            else:
                question = Question.query.filter_by(slug=object_id).first()
            
            if question is None:
                return send_error(message=messages.ERR_NOT_FOUND)
            
            current_user = g.current_user
            emails_or_usernames = data['emails_or_usernames']
            for email_or_username in emails_or_usernames:
                try:
                    user = User.query.filter(db.or_(User.display_name == email_or_username, User.email == email_or_username)).first()
                    if user is not None and user.id != current_user.id:
                        question.invited_users.append(user)

                except Exception as e:
                    print(e)
                    pass

            db.session.commit()
            return send_result()
        
        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_CREATE_FAILED.format(e))


    def decline_invited_question(self, object_id):
        try:
            current_user = g.current_user           
            result = None
            question_user_invite = QuestionUserInvite.query.filter_by(user_id=current_user.id, question_id=object_id).first()
            if question_user_invite:
                question_user_invite.status = 2
                result = question_user_invite._asdict()
            else:
                return send_error(message=messages.ERR_NOT_FOUND)
            db.session.commit()
            return send_result()
        
        except Exception as e:
            db.session.rollback()
            print(e)
            return send_error(message=messages.ERR_UPDATE_FAILED.format(e))


    def invite_friends(self, object_id):
        try:
            current_user = g.current_user
            emails_or_usernames = [friend.display_name for friend in current_user.friends]
            data = {}
            data['emails_or_usernames'] = emails_or_usernames
            return self.invite(object_id, data)
        
        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_CREATE_FAILED.format(e))


    def get_similar(self, args):
        if not 'title' in args:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('title'))

        title = args['title']
        limit = 30
        if args.get('limit'):
            limit = int(args['limit'])
        try:
            s = ESQuestion.search()
            q = Q("multi_match", query=title, fields=["title", "question"])
            s = s.query(q)
            s = s[0:limit]
            response = s.execute()
            hits = response.hits
            results = list()
            current_user = g.current_user
            for hit in hits:
                question_id = hit.meta.id
                question = Question.query.filter_by(id=question_id, is_private=False, is_deleted=False).first()
                if not question or question.title == title:
                    continue
                result = question._asdict()

                result['user'] = question.user
                result['topics'] = question.topics
                result['fixed_topic'] = question.fixed_topic                
                results.append(result)
            return send_result(data=marshal(results, QuestionDto.model_question_response))
        
        except Exception as e:
            print(e.__str__())
            return send_error(message=messages.ERR_GET_FAILED.format(e))


    def get_proposals(self, object_id, args):
        try:
            if object_id is None:
                return send_error(message=messages.ERR_PLEASE_PROVIDE.format('id'))

            if object_id.isdigit():
                question = Question.query.filter_by(id=object_id).first()
            else:
                question = Question.query.filter_by(slug=object_id).first()
            if question is None:
                return send_error(message=messages.ERR_NOT_FOUND)
            
            from_date, to_date = None, None

            if args.get('from_date'):
                try:
                    from_date = dateutil.parser.isoparse(args['from_date'])
                except Exception as e:
                    print(e.__str__())
                    pass
            if args.get('to_date'):
                try:
                    to_date = dateutil.parser.isoparse(args['to_date'])
                except Exception as e:
                    print(e.__str__())
                    pass
            query = QuestionProposal.query.filter(QuestionProposal.question_id == question.id)
            if from_date is not None:
                query = query.filter(QuestionProposal.proposal_created_date >= from_date)
            if to_date is not None:
                query = query.filter(QuestionProposal.proposal_created_date <= to_date)

            proposals = query.all()
            
            return send_result(data=marshal(proposals, QuestionDto.model_question_proposal_response))
        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_GET_FAILED.format(e))


    def create_question_deletion_proposal(self, object_id):

        if object_id is None:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('id'))

        try:
            if object_id.isdigit():
                question = Question.query.filter_by(id=object_id).first()
            else:
                question = Question.query.filter_by(slug=object_id).first()
            
            if question is None or question.is_deleted is True:
                return send_error(message=messages.ERR_NOT_FOUND)

            question_deletion_proposal = QuestionProposal.query.filter_by(question_id=question.id, is_parma_delete=1, is_approved=0).first()
            if question_deletion_proposal is not None:
                return send_error(message="Question deletion proposal ID {} has been sent and is pending!".format(object_id))

            proposal_data = question._asdict()
            proposal_data['is_parma_delete'] = True
            proposal_data['question_id'] = question.id
            proposal_data['topics'] = [topic.id for topic in question.topics]
            proposal = self._parse_proposal(data=proposal_data, proposal=None)
            db.session.add(proposal)
            db.session.commit()

            return send_result()
        
        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_CREATE_FAILED.format(e))

 
    def create_question_update_proposal(self, object_id, data):
        try:
            if object_id is None:
                return send_error(message=messages.ERR_PLEASE_PROVIDE.format('id'))
            
            if not isinstance(data, dict):
                return send_error(message=messages.ERR_WRONG_DATA_FORMAT)
            
            question = None
            if object_id.isdigit():
                question = Question.query.filter_by(id=object_id).first()
            else:
                question = Question.query.filter_by(slug=object_id).first()
            
            if question is None or question.is_deleted is True:
                return send_error(message=messages.ERR_NOT_FOUND)

            data['question_id'] = question.id

            if 'title' in data:
                data['title'] = data['title'].strip().capitalize()
                
                if not data['title'].endswith('?'):
                    return send_error(message=messages.ERR_QUESTION_NOT_END_WITH_QUESION_MARK)         

            proposal_data = question._asdict()
            proposal_data['question_id'] = question.id
            proposal_data['topics'] = [topic.id for topic in question.topics]
            proposal = self._parse_proposal(data=proposal_data, proposal=None)
            proposal = self._parse_proposal(data=data, proposal=proposal)

            proposal.last_activity = datetime.utcnow()
            proposal.slug = slugify(proposal.title)
            db.session.add(proposal)
            db.session.commit()
            return send_result()
        
        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_CREATE_FAILED.format(e))


    def approve_proposal(self, object_id):
        try:
            if object_id is None:
                return send_error(message=messages.ERR_PLEASE_PROVIDE.format('id'))

            proposal = QuestionProposal.query.filter_by(id=object_id).first()
            if proposal is None:
                return send_error(message=messages.ERR_NOT_FOUND)
            
            if proposal.is_approved:
                return send_result(message="Proposal ID {} is already approved".format(object_id))

            related_question = Question.query.filter_by(id=proposal.question_id).first()
            if related_question is None or related_question.is_deleted is True:
                return send_error(message="Question with the ID {} not found or has been deleted!".format(proposal.question_id))

            question_data = proposal._asdict()
            if proposal.is_parma_delete: 
                self.delete(str(proposal.question_id))
            else:                
                question = self._parse_question(data=question_data, question=related_question)
                question.last_activity = datetime.utcnow()

            proposal.is_approved = True
            db.session.commit()
            return send_result(data=marshal(question, QuestionDto.model_question_response))
        
        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_CREATE_FAILED.format(e))


    def update(self, object_id, data):

        if object_id is None:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('id'))
        
        if not isinstance(data, dict):
            return send_error(message=messages.ERR_WRONG_DATA_FORMAT)
        
        # Handling question title
        if 'title' in data:
            data['title'] = data['title'].strip().capitalize()
            if not data['title'].endswith('?'):
                return send_error(message=messages.ERR_QUESTION_NOT_END_WITH_QUESION_MARK)

        if object_id.isdigit():
            question = Question.query.filter_by(id=object_id).first()
        else:
            question = Question.query.filter_by(slug=object_id).first()
        
        if question is None:
            return send_error(message=messages.ERR_NOT_FOUND)

        #handling user
        current_user = g.current_user
        if question.user_id != current_user.id and not UserRole.is_admin(current_user.admin):
            return send_error(code=401, message=messages.ERR_NOT_AUTHORIZED)

        question = self._parse_question(data=data, question=question)
        try:

            question.updated_date = datetime.utcnow()
            question.last_activity = datetime.utcnow()
            question.slug = slugify(question.title)
            db.session.flush()
            # index to ES server
            question_dsl = ESQuestion(_id=question.id)
            question_dsl.update(question=strip_tags(question.question), title=question.title, slug=question.slug, updated_date=question.updated_date)

            db.session.commit()
            cache.clear_cache(Question.__class__.__name__)
            result = question._asdict()
            return send_result(data=marshal(result, QuestionDto.model_question_create_update_response))
        
        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_UPDATE_FAILED.format(e))


    def delete(self, object_id):

        if object_id is None:
            return send_error(message=messages.ERR_PLEASE_PROVIDE.format('id'))

        try:
            if object_id.isdigit():
                question = Question.query.filter_by(id=object_id).first()
            else:
                question = Question.query.filter_by(slug=object_id).first()
            
            if question is None:
                return send_error(message=messages.ERR_NOT_FOUND)

            #handling user
            current_user = g.current_user
            if not UserRole.is_admin(current_user.admin):
                return send_error(code=401, message=messages.ERR_NOT_AUTHORIZED)

            db.session.delete(question)

            # delete from question Es index
            question_dsl = ESQuestion(_id=question.id)
            question_dsl.delete()
            db.session.commit()
            cache.clear_cache(Question.__class__.__name__)

            return send_result()
        
        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_DELETE_FAILED.format(e))


    def apply_filtering(self, query, params):
        try: 
            query = super().apply_filtering(query, params)
            current_user = g.current_user
            if current_user:
                if not current_user.show_nsfw:
                    query = query.filter(Question.fixed_topic.has(db.func.coalesce(Topic.is_nsfw, False) == False))\
                        .filter(db.or_(db.not_(Question.topics.any()), Question.topics.any(Topic.is_nsfw == False)))

            get_my_own = False
            if params.get('user_id'):
                if current_user:
                    if params.get('user_id') == str(current_user.id):
                        get_my_own = True
                if not get_my_own:
                    query = query.filter(db.func.coalesce(Question.is_anonymous, False) != True)
            if not get_my_own:
                query = query.filter(db.func.coalesce(Question.is_private, False) != True)

            if params.get('title'):
                query = query.filter(Question.title.like(params.get('title')))
            
            if params.get('from_date'):
                query = query.filter(Question.created_date >= params.get('from_date'))
            
            if params.get('to_date'):
                query = query.filter(Question.created_date <= params.get('to_date'))
            
            if params.get('topic_id'):
                query = query.filter(Question.topics.any(Topic.id.in_(params.get('topic_id'))))

            if params.get('is_shared') and current_user:
                query = query.filter(Question.question_shares.any(QuestionShare.user_shared_to_id == current_user.id))
            return query

        except Exception as e:
            print(e.__str__())
            raise e


    def get_query(self):
        query = super().get_query()
        query = query.join(User, isouter=True).filter(db.or_(Question.user == None, User.is_deactivated == False))        
        return query


    def _parse_question(self, data, question=None):
        if question is None:
            question = Question()

        if 'title' in data:
            try:
                question.title = data['title']
            except Exception as e:
                print(e.__str__())
                pass            

        if 'question' in data:
            try:
                question.question = data['question']
            except Exception as e:
                print(e.__str__())
                pass

        if 'user_id' in data:
            try:
                question.user_id = data['user_id']
            except Exception as e:
                print(e.__str__())
                pass

        if 'fixed_topic_id' in data:
            try:
                question.fixed_topic_id = int(data['fixed_topic_id'])
            except Exception as e:
                print(e.__str__())
                pass

        if 'accepted_question_id' in data:
            try:
                question.accepted_question_id = int(data['accepted_question_id'])
            except Exception as e:
                print(e.__str__())
                pass

        if 'allow_video_answer' in data:
            try:
                question.allow_video_answer = bool(data['allow_video_answer'])
            except Exception as e:
                question.allow_video_answer = True
                print(e.__str__())
                pass

        if 'allow_audio_answer' in data:
            try:
                question.allow_audio_answer = bool(data['allow_audio_answer'])
            except Exception as e:
                question.allow_audio_answer = True
                print(e.__str__())
                pass

        if 'is_private' in data:
            try:
                question.is_private = bool(data['is_private'])
            except Exception as e:
                question.is_private = False
                print(e.__str__())
                pass

        if 'is_anonymous' in data:
            try:
                question.is_anonymous = bool(data['is_anonymous'])
            except Exception as e:
                question.is_anonymous = False
                print(e.__str__())
                pass

        if 'allow_comments' in data:
            try:
                question.allow_comments = bool(data['allow_comments'])
            except Exception as e:
                question.allow_comments = False
                print(e.__str__())
                pass

        if g.current_user_is_admin:
            if 'allow_voting' in data:
                try:
                    question.allow_voting = bool(data['allow_voting'])
                except Exception as e:
                    question.allow_voting = False
                    print(e.__str__())
                    pass

        topic_ids = None
        if 'topics' in data:
            topic_ids = data['topics']
            topics = []
            for topic_id in topic_ids:
                try:
                    topic = Topic.query.filter_by(id=topic_id).first()
                    topics.append(topic)
                except Exception as e:
                    print(e)
                    pass
            question.topics = topics

        return question


    def _parse_proposal(self, data, proposal=None):
        if proposal is None:
            proposal = QuestionProposal()

        if 'question_id ' in data:
            try:
                proposal.question_id = data['question_id']
            except Exception as e:
                print(e.__str__())
                pass
        
        if 'title' in data:
            try:
                proposal.title = data['title']
            except Exception as e:
                print(e.__str__())
                pass

        if 'question' in data:
            try:
                proposal.question = data['question']
            except Exception as e:
                print(e.__str__())
                pass

        if 'slug' in data:
            try:
                proposal.slug = data['slug']
            except Exception as e:
                print(e.__str__())
                pass

        if 'user_id' in data:
            try:
                proposal.user_id = data['user_id']
            except Exception as e:
                print(e.__str__())
                pass

        if 'fixed_topic_id' in data:
            try:
                proposal.fixed_topic_id = int(data['fixed_topic_id'])
            except Exception as e:
                print(e.__str__())
                pass
        
        if 'allow_video_question' in data:
            try:
                proposal.allow_video_question = bool(data['allow_video_question'])
            except Exception as e:
                proposal.allow_video_question = True
                print(e.__str__())
                pass

        if 'allow_audio_question' in data:
            try:
                proposal.allow_audio_question = bool(data['allow_audio_question'])
            except Exception as e:
                proposal.allow_audio_question = True
                print(e.__str__())
                pass

        if 'is_private' in data:
            try:
                proposal.is_private = bool(data['is_private'])
            except Exception as e:
                proposal.is_private = False
                print(e.__str__())
                pass
                
        if 'is_anonymous' in data:
            try:
                proposal.is_anonymous = bool(data['is_anonymous'])
            except Exception as e:
                proposal.is_anonymous = False
                print(e.__str__())
                pass

        if 'is_parma_delete' in data:
            try:
                proposal.is_parma_delete = bool(data['is_parma_delete'])
            except Exception as e:
                proposal.is_parma_delete = False
                print(e.__str__())
                pass

        if 'allow_comments' in data:
            try:
                proposal.allow_comments = bool(data['allow_comments'])
            except Exception as e:
                proposal.allow_comments = False
                print(e.__str__())
                pass

        if g.current_user_is_admin:
            if 'allow_voting' in data:
                try:
                    proposal.allow_voting = bool(data['allow_voting'])
                except Exception as e:
                    proposal.allow_voting = False
                    print(e.__str__())
                    pass

        topic_ids = None
        if 'topics' in data:
            topic_ids = data['topics']
            topics = []
            for topic_id in topic_ids:
                try:
                    topic = Topic.query.filter_by(id=topic_id).first()
                    topics.append(topic)
                except Exception as e:
                    print(e)
                    pass
            proposal.topics = topics

        return proposal


    def update_slug(self):
        questions = Question.query.all()
        try:
            for question in questions:
                question.slug = slugify(question.title)
                db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message=messages.ERR_CREATE_FAILED.format(e))
