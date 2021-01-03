#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from common.utils.util import send_question_invite_notif_email
from common.utils.onesignal_notif import push_notif_to_specific_users
import json
import re
from datetime import datetime

# third-party modules
import dateutil.parser
from bs4 import BeautifulSoup
from flask import current_app, g, request
from flask_restx import marshal
from slugify import slugify
from sqlalchemy import desc, func, or_, text

# own modules
from common.db import db
from app.modules.q_a.question.question_dto import QuestionDto
from common.controllers.controller import Controller
from common.enum import VotingStatusEnum
from common.utils.checker import check_spelling
from common.utils.response import paginated_result, send_error, send_result
from common.utils.sensitive_words import check_sensitive
from common.dramatiq_producers import new_question_notify_user_list, update_seen_questions

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


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
QuestionFavorite = db.get_model('QuestionFavorite')
QuestionBookmark = db.get_model('QuestionBookmark')
QuestionVote = db.get_model('QuestionVote')


class QuestionController(Controller):
    query_classname = 'Question'
    special_filtering_fields = ['from_date', 'to_date', 'title', 'topic_id', 'is_shared', 'is_created_by_friend', 'hot', 'for_me']
    allowed_ordering_fields = ['created_date', 'updated_date', 'upvote_count', 'comment_count', 'share_count', 'favorite_count', 'answers_count']
    
    def create(self, data):
        if not isinstance(data, dict):
            return send_error(message="Data is not correct or not in dictionary form")
        if not 'title' in data:
            return send_error(message='Question must contain at least the title.')

        current_user, _ = current_app.get_logged_user(request)
        if current_user:
            data['user_id'] = current_user.id

        try:
            if not data['title'].strip().endswith('?'):
                return send_error(message='Please end question title with question mark ("?")')
            data['title'] = re.sub(r"[-()\"#/@;:<>{}`+=~|.!?,]", "", data['title'])
            data['title'] = data['title'].strip()
            is_sensitive = check_sensitive(data['title'])
            if is_sensitive:
                return send_error(message='Nội dung câu hỏi của bạn không hợp lệ.')
            data['title'] = data['title'] + ' ?'
            title = data['title']
            user_id = data.get('user_id')
            question = Question.query.filter(Question.title == title).first()
            if not question:  # the topic does not exist
                question, topic_ids = self._parse_question(data=data, question=None)
                if question.topics.count('1') > 5:
                    return send_error(message='Question cannot have more than 5 topics.')
                spelling_errors = check_spelling(question.title)
                if len(spelling_errors) > 0:
                    return send_error(message='Please check question title for spelling errors', data=spelling_errors)
                if question.question:
                    is_sensitive = check_sensitive(' '.join(BeautifulSoup(question.question, "html.parser").stripped_strings))
                    if is_sensitive:
                        return send_error(message='Nội dung câu hỏi của bạn không hợp lệ.')
                question.created_date = datetime.utcnow()
                question.last_activity = datetime.utcnow()
                question.slug = slugify(question.title)
                db.session.add(question)
                db.session.commit()
                # Add topics and get back list of topic for question
                try:
                    result = question._asdict()
                    # get user info
                    result['user'] = question.user
                    result['topics'] = question.topics
                    result['fixed_topic'] = question.fixed_topic
                    # them thong tin nguoi dung dang upvote hay downvote cau hoi nay
                    result['up_vote'] = False
                    result['down_vote'] = False
                    followers = UserFollow.query.with_entities(UserFollow.follower_id)\
                        .filter(UserFollow.followed_id == question.user.id).all()
                    follower_ids = [follower[0] for follower in followers]
                    new_question_notify_user_list.send(question.id, follower_ids)
                    g.friend_belong_to_user_id = question.user.id
                    friends = UserFriend.query\
                        .filter(\
                            (UserFriend.friended_id == question.user.id) | \
                            (UserFriend.friend_id == question.user.id))\
                        .all()
                    friend_ids = [friend.adaptive_friend_id for friend in friends]
                    new_question_notify_user_list.send(question.id, friend_ids)
                    return send_result(message='Question was created successfully.',
                                       data=marshal(result, QuestionDto.model_question_response))
                except Exception as e:
                    print(e.__str__())
                    return send_result(data=marshal(question, QuestionDto.model_question_response),
                                       message='Question added, but could not add topics. Please update list topics later.')
            else:  # topic already exist
                return send_error(message='You already created the question with title {}.'.format(data['title']))
        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message='Could not create question. Contact administrator for solution.')

    def apply_filtering(self, query, params):
        query = super().apply_filtering(query, params)
        current_user = g.current_user
        if current_user:
            if not current_user.show_nsfw:
                query = query.filter(Question.fixed_topic.has(db.func.coalesce(Topic.is_nsfw, False) != True))\
                    .filter(db.or_(db.not_(Question.topics.any()), Question.topics.any(Topic.is_nsfw != True)))

        get_my_own = False
        if params.get('user_id'):
            user_id = int(params['user_id'])
            if current_user:
                if user_id == current_user.id:
                    get_my_own = True
            if not get_my_own:
                query = query.filter(db.func.coalesce(Question.is_anonymous, False) != True)
        if not get_my_own:
            query = query.filter(db.func.coalesce(Question.is_private, False) != True)

        if params.get('title'):
            title_similarity = db.func.SIMILARITY_STRING(Question.title, params.get('title')).label('title_similarity')
            query = query.filter(title_similarity > 50)
        if params.get('from_date'):
            query = query.filter(Question.created_date >= params.get('from_date'))
        if params.get('to_date'):
            query = query.filter(Question.created_date <= params.get('to_date'))
        if params.get('topic_id'):
            query = query.filter(Question.topics.any(Topic.id.in_(params.get('topic_id'))))
        if params.get('for_me') and current_user:
            query = query.filter((Question.invited_users.any(User.id==current_user.id)) | (Question.bookmarked_users.any(User.id==current_user.id)))
        if params.get('is_shared') and current_user:
            query = query.filter(Question.question_shares.any(QuestionShare.user_shared_to_id == current_user.id))
        if params.get('is_created_by_friend') and current_user:
            query = query\
                .join(UserFollow,(UserFollow.followed_id==Question.user_id), isouter=True)\
                .join(UserFriend,((UserFriend.friended_id==Question.user_id) | (UserFriend.friend_id==Question.user_id)), isouter=True)\
                .filter(
                    (UserFollow.follower_id == current_user.id) |
                    ((UserFriend.friended_id == current_user.id) | (UserFriend.friend_id == current_user.id)) |
                    (Question.question_shares.any(QuestionShare.user_shared_to_id == current_user.id))
                )
        if params.get('hot'):
            if g.current_user:
                query = query.join(TopicBookmark, \
                        ((TopicBookmark.topic_id==Question.fixed_topic_id) &\
                            TopicBookmark.user_id == current_user.id), \
                        isouter=True)\
                    .order_by(desc(func.field(TopicBookmark.user_id, g.current_user.id)),\
                        desc(text("upvote_count + downvote_count + share_count + favorite_count")))
            else:
                query = query.\
                    order_by(\
                        desc(text("upvote_count + downvote_count + share_count + favorite_count")))
        

        return query

    def get_query(self):
        query = self.get_model_class().query
        query = query.join(User, isouter=True).filter(db.or_(Question.user == None, User.is_deactivated != True))
        
        return query

    def get(self, args):
        try:
            query = self.get_query_results(args)
            res, code = paginated_result(query)
            current_user = g.current_user
            results = []
            for question in res.get('data'):
                result = question._asdict()
                # get user info
                result['user'] = question.user
                result['fixed_topic'] = question.fixed_topic
                result['topics'] = question.topics
                if current_user:
                    vote = QuestionVote.query.filter(QuestionVote.user_id == current_user.id, QuestionVote.question_id == question.id).first()
                    if vote is not None:
                        result['up_vote'] = True if VotingStatusEnum(2).name == vote.vote_status.name else False
                        result['down_vote'] = True if VotingStatusEnum(3).name == vote.vote_status.name else False
                    favorite = QuestionFavorite.query.filter(QuestionFavorite.user_id == current_user.id,
                                                    QuestionFavorite.question_id == question.id).first()
                    result['is_favorited_by_me'] = True if favorite else False
                    bookmark = QuestionBookmark.query.filter(QuestionBookmark.user_id == current_user.id,
                                                    QuestionBookmark.question_id == question.id).first()
                    result['is_bookmarked_by_me'] = True if bookmark else False
                results.append(result)
            res['data'] = marshal(results, QuestionDto.model_question_response)
            return res, code
        except Exception as e:
            print(e.__str__())
            return send_error(message="Could not load questions. Contact your administrator for solution.")

    def get_by_id(self, object_id):
        if object_id is None:
            return send_error("Question ID is null")
        if object_id.isdigit():
            question = Question.query.filter_by(id=object_id).first()
        else:
            question = Question.query.filter_by(slug=object_id).first()
        if question is None:
            return send_error(message='Could not find question with the ID {}'.format(object_id))
        current_user = g.current_user
        if question.is_private:
            if current_user:
                if not current_user == question.user:
                    if not question.invited_users.contains(current_user):
                        return send_error(message='Question is invitations only.')
            else:
                return send_error(message='Question is invitations only.') 
        result = question._asdict()
        # get user info
        result['user'] = question.user
        result['topics'] = question.topics
        result['fixed_topic'] = question.fixed_topic
        # lay them thong tin nguoi dung dang upvote hay downvote cau hoi nay
        if current_user:
            vote = QuestionVote.query.filter(QuestionVote.user_id == current_user.id, QuestionVote.question_id == question.id).first()
            if vote is not None:
                result['up_vote'] = True if VotingStatusEnum(2).name == vote.vote_status.name else False
                result['down_vote'] = True if VotingStatusEnum(3).name == vote.vote_status.name else False
            favorite = QuestionFavorite.query.filter(QuestionFavorite.user_id == current_user.id,
                                            QuestionFavorite.question_id == question.id).first()
            result['is_favorited_by_me'] = True if favorite else False
            bookmark = QuestionBookmark.query.filter(QuestionBookmark.user_id == current_user.id,
                                            QuestionBookmark.question_id == question.id).first()
            result['is_bookmarked_by_me'] = True if bookmark else False
            update_seen_questions.send(question.id, current_user.id)
        return send_result(data=marshal(result, QuestionDto.model_question_response), message='Success')

    def invite(self, object_id, data):
        try:
            if not 'emails_or_usernames' in data:
                return send_error(message='Please provide emails or usernames.')
            if object_id is None:
                return send_error("Question ID is null")
            if object_id.isdigit():
                question = Question.query.filter_by(id=object_id).first()
            else:
                question = Question.query.filter_by(slug=object_id).first()
            if question is None:
                return send_error(message='Could not find question with the ID {}'.format(object_id))
            current_user, _ = current_app.get_logged_user(request)
            emails_or_usernames = data['emails_or_usernames']
            for email_or_username in emails_or_usernames:
                try:
                    user = User.query.filter(db.or_(User.display_name == email_or_username, User.email == email_or_username)).first()
                    if user:
                        question.invited_users.append(user)
                        
                        if user:
                            if user.is_online\
                                and user.question_invite_notify_settings:
                                display_name =  question.user.display_name if question.user else 'Khách'
                                message = '[Thông báo] ' + display_name + ' đã mời bạn trả lời!'
                                push_notif_to_specific_users(message, [user.id])
                            elif user.question_invite_email_settings:
                                send_question_invite_notif_email(user, current_user, question)
                except Exception as e:
                    print(e)
                    pass
            db.session.commit()
            result = question._asdict()
            result['user'] = question.user
            result['topics'] = question.topics
            result['fixed_topic'] = question.fixed_topic
            # lay them thong tin nguoi dung dang upvote hay downvote cau hoi nay
            if current_user:
                vote = QuestionVote.query.filter(QuestionVote.user_id == current_user.id, QuestionVote.question_id == question.id).first()
                if vote is not None:
                    result['up_vote'] = True if VotingStatusEnum(2).name == vote.vote_status.name else False
                    result['down_vote'] = True if VotingStatusEnum(3).name == vote.vote_status.name else False
                favorite = QuestionFavorite.query.filter(QuestionFavorite.user_id == current_user.id,
                                                QuestionFavorite.question_id == question.id).first()
                result['is_favorited_by_me'] = True if favorite else False
                bookmark = QuestionBookmark.query.filter(QuestionBookmark.user_id == current_user.id,
                                                QuestionBookmark.question_id == question.id).first()
                result['is_bookmarked_by_me'] = True if bookmark else False
            return send_result(data=marshal(result, QuestionDto.model_question_response), message='Success')
        except Exception as e:
            print(e)
            return send_error(message="Invite failed. Error: " + e.__str__())

    def invite_friends(self, object_id):
        try:
            current_user = g.current_user
            emails_or_usernames = [friend.display_name for friend in current_user.friends]
            data = {}
            data['emails_or_usernames'] = emails_or_usernames
            return self.invite(object_id, data)
        except Exception as e:
            print(e)
            return send_error(message="Invite failed. Error: " + e.__str__())

    def get_similar(self, args):
        if not 'title' in args:
            return send_error(message='Please provide at least the title.')
        title = args['title']
        if args.get('limit'):
            limit = int(args['limit'])
        else:
            return send_error(message='Please provide limit')
        
        try:
            current_user, _ = current_app.get_logged_user(request)
            query = Question.query.filter_by(is_private=False)  # query search from view
            if args.get('exclude_question_id'):
                query = query.filter(Question.id != args.get('exclude_question_id'))
            title_similarity = db.func.SIMILARITY_STRING(Question.title, title).label('title_similarity')
            questions = query.with_entities(Question, title_similarity)\
                .filter(title_similarity > args.get('similarity_rate'))\
                .order_by(desc(title_similarity))\
                .limit(limit)\
                .all()
            results = list()
            for question in questions:
                question = question[0]
                result = question._asdict()
                # get user info
                result['user'] = question.user
                result['topics'] = question.topics
                result['fixed_topic'] = question.fixed_topic
                # lay them thong tin nguoi dung dang upvote hay downvote cau hoi nay
                if current_user:
                    vote = QuestionVote.query.filter(QuestionVote.user_id == current_user.id, QuestionVote.question_id == question.id).first()
                    if vote is not None:
                        result['up_vote'] = True if VotingStatusEnum(2).name == vote.vote_status.name else False
                        result['down_vote'] = True if VotingStatusEnum(3).name == vote.vote_status.name else False
                    favorite = QuestionFavorite.query.filter(QuestionFavorite.user_id == current_user.id,
                                                    QuestionFavorite.question_id == question.id).first()
                    result['is_favorited_by_me'] = True if favorite else False
                    bookmark = QuestionBookmark.query.filter(QuestionBookmark.user_id == current_user.id,
                                                    QuestionBookmark.question_id == question.id).first()
                    result['is_bookmarked_by_me'] = True if bookmark else False
                    # vote = QuestionVote.query.filter(QuestionVote.user_id == current_user.id, QuestionVote.question_id == question.id).first()
                    # if vote is not None:
                    #     result['up_vote'] = vote.up_vote
                    #     result['down_vote'] = vote.down_vote
                results.append(result)
            return send_result(data=marshal(results, QuestionDto.model_question_response), message='Success')
        except Exception as e:
            print(e)
            return send_error(message="Get similar questions failed. Error: "+ e.__str__())

    def get_recommended_users(self, args):
        try:
            if args.get('limit'):
                limit = int(args['limit'])
            else:
                return send_error(message='Please provide limit')
            if args.get('topic'):
                topics = args['topic']
            else:
                topics = []
            top_users_reputation = Reputation.query.with_entities(
                    Reputation.user_id,
                    User,
                    db.func.sum(Reputation.score).label('total_score'),
                )\
                .join(Reputation.user)\
                .group_by(Reputation.user_id, User)\
                .filter(Reputation.topic_id.in_(topics))\
                .order_by(desc('total_score'))\
                .limit(limit).all()
            results = [{'user_id': user_id, 'user': user._asdict(), 'total_score': total_score} for user_id, user, total_score in top_users_reputation]
            return send_result(data=marshal(results, QuestionDto.top_user_reputation_response), message='Success')
        except Exception as e:
            print(e)
            return send_error(message="Get recommended users failed. Error: " + e.__str__())

    def get_recommended_topics(self, args):
        if not 'title' in args:
            return send_error(message='Please provide at least the title.')
        title = args['title']
        if not 'limit' in args:
            return send_error(message='Please provide limit')
        limit = int(args['limit'])
        
        try:
            current_user, _ = current_app.get_logged_user(request)
            title_similarity = db.func.SIMILARITY_STRING(Question.title, title).label('title_similarity')
            query = Topic.query.distinct()\
                .join(Question, isouter=True)\
                .with_entities(Topic, title_similarity)\
                .filter(db.text('IFNULL(is_private, False)') == False)\
                .filter(title_similarity > 50)\
                .order_by(desc(title_similarity))\
                .limit(limit)
            topics = [topic[0] for topic in query.all()]
            return send_result(data=marshal(topics, QuestionDto.model_topic), message='Success')
        except Exception as e:
            print(e)
            return send_error(message="Get similar questions failed. Error: "+ e.__str__())

    def get_proposals(self, object_id, args):
        try:
            if object_id is None:
                return send_error(message="Question ID is null")
            if object_id.isdigit():
                question = Question.query.filter_by(id=object_id).first()
            else:
                question = Question.query.filter_by(slug=object_id).first()
            if question is None:
                return send_error(message="Question with the ID {} not found".format(object_id))
            
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
            
            return send_result(message='Question update proposal was created successfully.',
                                data=marshal(proposals, QuestionDto.model_question_proposal_response))
        except Exception as e:
            print(e.__str__())
            return send_error(message='Could not get proposals. Error: ' + e.__str__())
    
    def create_delete_proposal(self, object_id):
        try:
            if object_id is None:
                return send_error(message="Question ID is null")
            if object_id.isdigit():
                question = Question.query.filter_by(id=object_id).first()
            else:
                question = Question.query.filter_by(slug=object_id).first()
            if question is None:
                return send_error(message="Question with the ID {} not found".format(object_id))

            data = {}
            data['question_id'] = question.id
            data['is_parma_delete'] = True
            proposal, _ = self._parse_proposal(data=data, proposal=None)
            db.session.add(proposal)
            db.session.commit()
            return send_result(message='Question update proposal was created successfully.',
                                data=marshal(proposal, QuestionDto.model_question_proposal_response))
        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message='Could not create question. Contact administrator for solution.')
    
    def create_proposal(self, object_id, data):
        try:
            if object_id is None:
                return send_error(message="Question ID is null")
            if not isinstance(data, dict):
                return send_error(message="Data is not in dictionary form.")
            if object_id.isdigit():
                question = Question.query.filter_by(id=object_id).first()
            else:
                question = Question.query.filter_by(slug=object_id).first()
            if question is None:
                return send_error(message="Question with the ID {} not found".format(object_id))

            data['question_id'] = question.id
            proposal_data = question._asdict()
            proposal_data['question_id'] = question.id
            proposal_data['topics'] = [topic.id for topic in question.topics]
            proposal, _ = self._parse_proposal(data=proposal_data, proposal=None)
            proposal, _ = self._parse_proposal(data=data, proposal=proposal)

            if proposal.topics.count('1') > 5:
                return send_error(message='Question cannot have more than 5 topics.')
            if not proposal.title.strip().endswith('?'):
                return send_error(message='Please end question title with questio mark ("?")')
            spelling_errors = check_spelling(proposal.title)
            if len(spelling_errors) > 0:
                return send_error(message='Please check question title for spelling errors', data=spelling_errors)
            if proposal.question:
                is_sensitive = check_sensitive(' '.join(BeautifulSoup(proposal.question, "html.parser").stripped_strings))
                if is_sensitive:
                    return send_error(message='Question body not allowed.')
            proposal.last_activity = datetime.utcnow()
            proposal.slug = slugify(question.title)
            db.session.add(proposal)
            db.session.commit()
            return send_result(message='Question update proposal was created successfully.',
                                data=marshal(proposal, QuestionDto.model_question_proposal_response))
        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message='Could not create question. Contact administrator for solution.')
    
    def approve_proposal(self, object_id):
        try:
            if object_id is None:
                return send_error(message="Proposal ID is null")
            proposal = QuestionProposal.query.filter_by(id=object_id).first()
            if proposal is None:
                return send_error(message="Proposal with the ID {} not found".format(object_id))
            if proposal.is_approved:
                return send_result(message="Proposal with the ID {} is already approved".format(object_id))

            question_data = proposal._asdict()
            if proposal.is_parma_delete:
                proposal.is_approved = True
                return self.delete(str(proposal.question_id))
            related_question = Question.query.filter_by(id=proposal.question_id).first()
            if related_question is None:
                return send_error(message="Question with the ID {} not found".format(proposal.question_id))
            question, _ = self._parse_question(data=question_data, question=related_question)
            question.last_activity = datetime.utcnow()
            proposal.is_approved = True
            db.session.commit()
            return send_result(message='Question update proposal was approved successfully.',
                                data=marshal(question, QuestionDto.model_question_response))
        except Exception as e:
            db.session.rollback()
            print(e.__str__())
            return send_error(message='Could approve question proposal. Contact administrator for solution.')

    def update(self, object_id, data):
        """ Thuc hien update nhu sau:
            Khi nguoi dung lua chon thay the hoac xoa topic khoi question thi thuc hien cap nhat vao bang question_topic.
        
        Args:
            object_id:
            data:
        
        Returns:
        """

        if object_id is None:
            return send_error(message="Question ID is null")
        if not isinstance(data, dict):
            return send_error(message="Data is not in dictionary form.")
        if object_id.isdigit():
            question = Question.query.filter_by(id=object_id).first()
        else:
            question = Question.query.filter_by(slug=object_id).first()
        if question is None:
            return send_error(message="Question with the ID {} not found".format(object_id))
        question, _ = self._parse_question(data=data, question=question)
        try:
            if question.topics.count('1') > 5:
                return send_error(message='Question cannot have more than 5 topics.')
            # check sensitive after updating
            is_sensitive = check_sensitive(question.title)
            if is_sensitive:
                return send_error(message='Không thể sửa câu hỏi vì nội dung mới của bạn không hợp lệ.')
            if question.question:
                is_sensitive = check_sensitive(' '.join(BeautifulSoup(question.question, "html.parser").stripped_strings))
                if is_sensitive:
                    return send_error(message='Không thể sửa câu hỏi vì nội dung mới của bạn không hợp lệ.')
            question.updated_date = datetime.utcnow()
            question.last_activity = datetime.utcnow()
            question.slug = slugify(question.title)
            db.session.commit()
            result = question._asdict()
            # get user info
            result['user'] = question.user
            result['topics'] = question.topics
            result['fixed_topic'] = question.fixed_topic
            # lay them thong tin nguoi dung dang upvote hay downvote cau hoi nay
            current_user, _ = current_app.get_logged_user(request)
            if current_user:
                vote = QuestionVote.query.filter(QuestionVote.user_id == current_user.id, QuestionVote.question_id == question.id).first()
                if vote is not None:
                    result['up_vote'] = True if VotingStatusEnum(2).name == vote.vote_status.name else False
                    result['down_vote'] = True if VotingStatusEnum(3).name == vote.vote_status.name else False
                favorite = QuestionFavorite.query.filter(QuestionFavorite.user_id == current_user.id,
                                                QuestionFavorite.question_id == question.id).first()
                result['is_favorited_by_me'] = True if favorite else False
                bookmark = QuestionBookmark.query.filter(QuestionBookmark.user_id == current_user.id,
                                                QuestionBookmark.question_id == question.id).first()
                result['is_bookmarked_by_me'] = True if bookmark else False
            return send_result(message="Update successfully",
                                data=marshal(result, QuestionDto.model_question_response))
        except Exception as e:
            print(e.__str__())
            return send_error(message='Could not update question.')

    def delete(self, object_id):
        """ Delete question permanently- only Admin is allowed to performed this action accordingly to hoovada.com policy
            User can only send delete request to Admin
        """
        try:
            if object_id.isdigit():
                question = Question.query.filter_by(id=object_id).first()
            else:
                question = Question.query.filter_by(slug=object_id).first()
            if question is None:
                return send_error(message="Question with ID {} not found".format(object_id))
            else:
                # delete from question_topic

                # delete from vote

                # delete from share

                # delete from answer

                # delete from timline

                # delete from

                db.session.delete(question)
                db.session.commit()
                return send_result(message="Question with the ID {} was deleted.".format(object_id))
        except Exception as e:
            print(e.__str__())
            return send_error(message="Could not delete question with ID {}".format(object_id))

    def _parse_question(self, data, question=None):
        if question is None:
            question = Question()
        if 'title' in data:
            question.title = data['title']
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
        if 'question' in data:
            question.question = data['question']
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
        if 'is_deleted' in data:
            try:
                question.is_deleted = bool(data['is_deleted'])
            except Exception as e:
                question.is_deleted = False
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
        topic_ids = None
        if 'topics' in data:
            topic_ids = data['topics']
            # update question topics
            topics = []
            for topic_id in topic_ids:
                try:
                    topic = Topic.query.filter_by(id=topic_id).first()
                    topics.append(topic)
                except Exception as e:
                    print(e)
                    pass
            question.topics = topics

        return question, topic_ids

    def _parse_proposal(self, data, proposal=None):
        if proposal is None:
            proposal = QuestionProposal()
        proposal.question_id = data['question_id']
        if 'title' in data:
            proposal.title = data['title']
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
        if 'question' in data:
            proposal.question = data['question']
        if 'accepted_question_id' in data:
            try:
                proposal.accepted_question_id = int(data['accepted_question_id'])
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
        if 'is_deleted' in data:
            try:
                proposal.is_deleted = bool(data['is_deleted'])
            except Exception as e:
                proposal.is_deleted = False
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
        topic_ids = None
        if 'topics' in data:
            topic_ids = data['topics']
            # update proposal topics
            topics = []
            for topic_id in topic_ids:
                try:
                    topic = Topic.query.filter_by(id=topic_id).first()
                    topics.append(topic)
                except Exception as e:
                    print(e)
                    pass
            proposal.topics = topics

        return proposal, topic_ids
        
    def update_slug(self):
        questions = Question.query.all()
        try:
            for question in questions:
                question.slug = slugify(question.title)
                db.session.commit()
        except Exception as e:
            print(e.__str__())
            pass
