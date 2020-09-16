#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
import json
from datetime import datetime

# third-party modules
import dateutil.parser
from flask import request
from flask_restx import marshal
from sqlalchemy import desc

# own modules
from app import db
from app.modules.auth.auth_controller import AuthController
from app.modules.common.controller import Controller
from app.modules.q_a.question.question import Question, QuestionProposal
from app.modules.q_a.question.favorite.favorite import QuestionFavorite
from app.modules.q_a.question.question_dto import QuestionDto
from app.modules.auth.auth_controller import AuthController
from app.modules.q_a.question.voting.vote import QuestionVote, VotingStatusEnum
from app.modules.topic.question_topic.question_topic import QuestionTopic
from app.modules.q_a.answer.answer import Answer
from app.modules.q_a.answer.answer_dto import AnswerDto
from app.modules.topic.topic import Topic
from app.modules.user.user import User
from app.modules.user.reputation.reputation import Reputation
from app.utils.response import send_error, send_result
from app.utils.sensitive_words import check_sensitive
from app.utils.checker import check_spelling
from slugify import slugify

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class QuestionController(Controller):
    def search(self, args):
        """ Search questions.
        NOTE: HIEN GIO SEARCH THEO FIXED_TOPIC_ID, SAU SE SUA LAI DE SEARCH THEO CA FIXED_TOPIC_ID VA TOPIC_ID, SU DUNG VIEW.

        Args:

        Returns:
        
        """
        query = Question.query # query search from view
        current_user, _ = AuthController.get_logged_user(request)

        if not isinstance(args, dict):
            return send_error(message='Could not parse the params.')
        title, user_id, fixed_topic_id, created_date, updated_date, from_date, to_date, anonymous, topic_ids = None, None, None, None, None, None, None, None, None
        if args.get('title'):
            title = args['title']
        if args.get('user_id'):
            try:
                user_id = int(args['user_id'])
                if current_user:
                    if user_id == current_user.id:
                        query = query.filter_by(is_private=False) 
            except Exception as e:
                print(e.__str__())
                pass
        if args.get('fixed_topic_id'):
            try:
                fixed_topic_id = int(args['fixed_topic_id'])
            except Exception as e:
                print(e.__str__())
                pass
        if args.get('created_date'):
            try:
                created_date = dateutil.parser.isoparse(args['created_date'])
            except Exception as e:
                print(e.__str__())
                pass
        if args.get('updated_date'):
            try:
                updated_date = dateutil.parser.isoparse(args['updated_date'])
            except Exception as e:
                print(e.__str__())
                pass
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
        if args.get('anonymous'):
            try:
                anonymous = int(args['anonymous'])
            except Exception as e:
                print(e.__str__())
                pass
        if args.get('topic_id'):
            try:
                topic_ids = args['topic_id']
            except Exception as e:
                print(e.__str__())
                pass
        if title is None and user_id is None and fixed_topic_id is None and created_date is None and updated_date is None and anonymous is None and topic_ids is None:
            send_error(message='Provide params to search.')
        is_filter = False
        if title is not None and not str(title).strip().__eq__(''):
            # title = '%' + title.strip() + '%'
            # query = query.filter(Question.title.like(title))
            title_similarity = db.func.SIMILARITY_STRING(title, Question.title).label('title_similarity')
            query = query.filter(title_similarity > 50)
            is_filter = True
        if user_id is not None:
            query = query.filter(Question.user_id == user_id)
            is_filter = True
        if fixed_topic_id is not None:
            query = query.filter(Question.fixed_topic_id == fixed_topic_id)
            is_filter = True
        if created_date is not None:
            query = query.filter(Question.created_date == created_date)
            is_filter = True
        if updated_date is not None:
            query = query.filter(Question.updated_date == updated_date)
            is_filter = True
        if from_date is not None:
            query = query.filter(Question.created_date >= from_date)
            is_filter = True
        if to_date is not None:
            query = query.filter(Question.created_date <= to_date)
            is_filter = True
        if topic_ids is not None:
            query = query.filter(Question.topics.any(Topic.id.in_(topic_ids)))
            is_filter = True
        if is_filter:
            questions = query.order_by(desc(Question.upvote_count)).all()
            if questions is not None and len(questions) > 0:
                results = list()
                for question in questions:
                    # kiem tra den topic
                    result = question._asdict()
                    # get user info
                    result['user'] = question.question_by_user
                    # get all topics that question belongs to
                    # question_id = question.id
                    # question_topics = QuestionTopic.query.filter_by(question_id=question_id).all()
                    # topics = list()
                    # for question_topic in question_topics:
                    #     topic_id = question_topic.topic_id
                    #     topic = Topic.query.filter_by(id=topic_id).first()
                    #     topics.append(topic)
                    result['topics'] = question.topics
                    # lay them thong tin nguoi dung dang upvote hay downvote cau hoi nay
                    if current_user:
                        vote = QuestionVote.query.filter(QuestionVote.user_id == current_user.id, QuestionVote.question_id == question.id).first()
                        if vote is not None:
                            result['up_vote'] = True if VotingStatusEnum(2).name == vote.vote_status.name else False
                            result['down_vote'] = True if VotingStatusEnum(3).name == vote.vote_status.name else False
                        favorite = QuestionFavorite.query.filter(QuestionFavorite.user_id == current_user.id,
                                                        QuestionFavorite.question_id == question.id).first()
                        result['is_favorited_by_me'] = True if favorite else False
                        # vote = QuestionVote.query.filter(QuestionVote.user_id == current_user.id, QuestionVote.question_id == question.id).first()
                        # if vote is not None:
                        #     result['up_vote'] = vote.up_vote
                        #     result['down_vote'] = vote.down_vote
                    results.append(result)
                return send_result(marshal(results, QuestionDto.model_question_response), message='Success')
            else:
                return send_result(message='Could not find any questions')
        else:
            return send_error(message='Could not find questions. Please check your parameters again.')

    def create(self, data):
        if not isinstance(data, dict):
            return send_error(message="Data is not correct or not in dictionary form")
        if not 'title' in data:
            return send_error(message='Question must contain at least the title.')

        current_user, _ = AuthController.get_logged_user(request)
        if current_user:
            data['user_id'] = current_user.id

        try:
            title = data['title']
            user_id = data.get('user_id')
            is_sensitive = check_sensitive(title)
            if is_sensitive:
                return send_error(message='Nội dung câu hỏi của bạn không hợp lệ.')
            question = Question.query.filter(Question.title == title).filter(Question.user_id == user_id).first()
            if not question:  # the topic does not exist
                question, topic_ids = self._parse_question(data=data, question=None)
                if question.topics.count('1') > 5:
                    return send_error(message='Question cannot have more than 5 topics.')
                if not question.title.strip().endswith('?'):
                    return send_error(message='Please end question title with questio mark ("?")')
                spelling_errors = check_spelling(question.title)
                if len(spelling_errors) > 0:
                    return send_error(message='Please check question title for spelling errors', data=spelling_errors)
                if question.question:
                    is_sensitive = check_sensitive(question.question)
                    if is_sensitive:
                        return send_error(message='Nội dung câu hỏi của bạn không hợp lệ.')
                question.created_date = datetime.utcnow()
                question.last_activity = datetime.utcnow()
                question.slug = slugify(question.title)
                db.session.add(question)
                db.session.commit()
                # # update question_count for fixed topic
                # try:
                #     fixed_topic_id = question.fixed_topic_id
                #     fixed_topic = Topic.query.filter_by(id=fixed_topic_id).first()
                #     fixed_topic.question_count += 1
                #     db.session.commit()
                # except Exception as e:
                #     print(e.__str__())
                #     pass
                # # update question_count for user
                # try:
                #     user = User.query.filter_by(id=user_id).first()
                #     user.question_count += 1
                #     db.session.commit()
                # except Exception as e:
                #     print(e.__str__())
                #     pass
                # Add topics and get back list of topic for question
                try:
                    result = question._asdict()
                    # get user info
                    # user = User.query.filter_by(id=question.user_id).first()
                    result['user'] = question.question_by_user
                    # add question_topics
                    # question_id = question.id
                    # topics = list()
                    # for topic_id in topic_ids:
                    #     question_topic = QuestionTopic(question_id=question_id, topic_id=topic_id)
                    #     db.session.add(question_topic)
                    #     db.session.commit()
                    #     topic = Topic.query.filter_by(id=topic_id).first()
                    #     # update question_count for current topic.
                    #     topic.question_count += 1
                    #     db.session.commit()
                    #     topics.append(topic)
                    result['topics'] = question.topics
                    # them thong tin nguoi dung dang upvote hay downvote cau hoi nay
                    result['up_vote'] = False
                    result['down_vote'] = False
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

    def get(self):
        try:
            current_user, _ = AuthController.get_logged_user(request)
            query = Question.query.filter_by(is_private=False)  # query search from view
            questions = query.order_by(desc(Question.upvote_count), desc(Question.created_date)).limit(50).all()
            # for question in questions:
            #     # # chay cau lenh de cap nhat la fixed_topic_name
            #     # fixed_topic_id = question.fixed_topic_id
            #     # fixed_topic = Topic.query.filter_by(id=fixed_topic_id).first()
            #     # if fixed_topic:
            #     #     question.fixed_topic_name = fixed_topic.name
            #     # question.views_count = 0
            #     # question.answers_count = 0
            #     # question.upvote_count = 0
            #     # question.downvote_count = 0
            #     # question.favorite_count = 0
            #     # question.share_count = 0
            #
            #     # update anonymous va user_hidden
            #     if question.user_id == 6:
            #         question.anonymous = 1
            #     else:
            #         question.anonymous = 0
            #     question.user_hidden = 0
            # db.session.commit()
            results = list()
            for question in questions:
                result = question._asdict()
                # get user info
                # user = User.query.filter_by(id=question.user_id).first()
                result['user'] = question.question_by_user

                # get all topics that question belongs to
                # question_id = question.id
                # question_topics = QuestionTopic.query.filter_by(question_id=question_id).all()
                # topics = list()
                # for question_topic in question_topics:
                #     topic_id = question_topic.topic_id
                #     topic = Topic.query.filter_by(id=topic_id).first()
                #     topics.append(topic)
                result['topics'] = question.topics
                # lay them thong tin nguoi dung dang upvote hay downvote cau hoi nay
                if current_user:
                    vote = QuestionVote.query.filter(QuestionVote.user_id == current_user.id, QuestionVote.question_id == question.id).first()
                    if vote is not None:
                        result['up_vote'] = True if VotingStatusEnum(2).name == vote.vote_status.name else False
                        result['down_vote'] = True if VotingStatusEnum(3).name == vote.vote_status.name else False
                    favorite = QuestionFavorite.query.filter(QuestionFavorite.user_id == current_user.id,
                                                    QuestionFavorite.question_id == question.id).first()
                    result['is_favorited_by_me'] = True if favorite else False
                    # vote = QuestionVote.query.filter(QuestionVote.user_id == current_user.id, QuestionVote.question_id == question.id).first()
                    # if vote is not None:
                    #     result['up_vote'] = vote.up_vote
                    #     result['down_vote'] = vote.down_vote
                results.append(result)
            return send_result(data=marshal(results, QuestionDto.model_question_response), message='Success')
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
        current_user, _ = AuthController.get_logged_user(request)
        if question.is_private:
            if not current_user == question.question_by_user:
                if not self.is_invited(question, current_user):
                    return send_error(message='Question is invitations only.')
        result = question._asdict()
        # get user info
        result['user'] = question.question_by_user
        # get all topics that question belongs to
        # question_id = question.id
        # question_topics = QuestionTopic.query.filter_by(question_id=question_id).all()
        # topics = list()
        # for question_topic in question_topics:
        #     topic_id = question_topic.topic_id
        #     topic = Topic.query.filter_by(id=topic_id).first()
        #     topics.append(topic)
        result['topics'] = question.topics
        # lay them thong tin nguoi dung dang upvote hay downvote cau hoi nay
        if current_user:
            vote = QuestionVote.query.filter(QuestionVote.user_id == current_user.id, QuestionVote.question_id == question.id).first()
            if vote is not None:
                result['up_vote'] = True if VotingStatusEnum(2).name == vote.vote_status.name else False
                result['down_vote'] = True if VotingStatusEnum(3).name == vote.vote_status.name else False
            favorite = QuestionFavorite.query.filter(QuestionFavorite.user_id == current_user.id,
                                            QuestionFavorite.question_id == question.id).first()
            result['is_favorited_by_me'] = True if favorite else False
            # vote = QuestionVote.query.filter(QuestionVote.user_id == current_user.id, QuestionVote.question_id == question.id).first()
            # if vote is not None:
            #     result['up_vote'] = vote.up_vote
            #     result['down_vote'] = vote.down_vote
        return send_result(data=marshal(result, QuestionDto.model_question_response), message='Success')

    def invite(self, object_id, data):
        try:
            if not 'emails_or_usernames' in data:
                return send_error(message='Question must contain at least the title.')
            if object_id is None:
                return send_error("Question ID is null")
            if object_id.isdigit():
                question = Question.query.filter_by(id=object_id).first()
            else:
                question = Question.query.filter_by(slug=object_id).first()
            if question is None:
                return send_error(message='Could not find question with the ID {}'.format(object_id))
            current_user, _ = AuthController.get_logged_user(request)
            emails_or_usernames = data['emails_or_usernames']
            for email_or_username in emails_or_usernames:
                try:
                    user = User.query.filter_by(display_name=email_or_username).first()
                    if not user:
                        user = User.query.filter_by(email=email_or_username).first()
                    if not user:
                        question.invited_users.append(user)
                except Exception as e:
                    print(e)
                    pass
            db.session.commit()
            result = question._asdict()
            result['user'] = question.question_by_user
            result['topics'] = question.topics
            # lay them thong tin nguoi dung dang upvote hay downvote cau hoi nay
            if current_user:
                vote = QuestionVote.query.filter(QuestionVote.user_id == current_user.id, QuestionVote.question_id == question.id).first()
                if vote is not None:
                    result['up_vote'] = True if VotingStatusEnum(2).name == vote.vote_status.name else False
                    result['down_vote'] = True if VotingStatusEnum(3).name == vote.vote_status.name else False
                favorite = QuestionFavorite.query.filter(QuestionFavorite.user_id == current_user.id,
                                                QuestionFavorite.question_id == question.id).first()
                result['is_favorited_by_me'] = True if favorite else False
                # vote = QuestionVote.query.filter(QuestionVote.user_id == current_user.id, QuestionVote.question_id == question.id).first()
                # if vote is not None:
                #     result['up_vote'] = vote.up_vote
                #     result['down_vote'] = vote.down_vote
            return send_result(data=marshal(result, QuestionDto.model_question_response), message='Success')
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
            current_user, _ = AuthController.get_logged_user(request)
            query = Question.query.filter_by(is_private=False)  # query search from view
            title_similarity = db.func.SIMILARITY_STRING(title, Question.title).label('title_similarity')
            questions = query.with_entities(Question, title_similarity)\
                .filter(title_similarity > 50)\
                .order_by(desc(title_similarity))\
                .limit(limit)\
                .all()
            results = list()
            for question in questions:
                question = question[0]
                result = question._asdict()
                # get user info
                result['user'] = question.question_by_user
                result['topics'] = question.topics
                # lay them thong tin nguoi dung dang upvote hay downvote cau hoi nay
                if current_user:
                    vote = QuestionVote.query.filter(QuestionVote.user_id == current_user.id, QuestionVote.question_id == question.id).first()
                    if vote is not None:
                        result['up_vote'] = True if VotingStatusEnum(2).name == vote.vote_status.name else False
                        result['down_vote'] = True if VotingStatusEnum(3).name == vote.vote_status.name else False
                    favorite = QuestionFavorite.query.filter(QuestionFavorite.user_id == current_user.id,
                                                    QuestionFavorite.question_id == question.id).first()
                    result['is_favorited_by_me'] = True if favorite else False
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
                return send_error(message='Please provide topics')

            top_users_reputation = db.session.query(
                    User,
                    db.func.sum(Reputation.score).label('total_score'),
                )\
                .filter(Reputation.topic_id.in_(topics))\
                .group_by(User,)\
                .order_by(desc('total_score'))\
                .limit(limit).all()
            results = [{'user': user, 'total_score': total_score} for user, total_score in top_users_reputation]
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
            current_user, _ = AuthController.get_logged_user(request)
            title_similarity = db.func.SIMILARITY_STRING(title, Question.title).label('title_similarity')
            query = Topic.query.distinct()\
                .join(Question)\
                .with_entities(Topic, title_similarity)\
                .filter(Question.is_private == False)\
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
                is_sensitive = check_sensitive(proposal.question)
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
                is_sensitive = check_sensitive(question.question)
                if is_sensitive:
                    return send_error(message='Không thể sửa câu hỏi vì nội dung mới của bạn không hợp lệ.')
            question.updated_date = datetime.utcnow()
            question.last_activity = datetime.utcnow()
            question.slug = slugify(question.title)
            db.session.commit()
            result = question._asdict()
            # get user info
            result['user'] = question.question_by_user
            # get all topics that question belongs to
            # question_id = question.id
            # question_topics = QuestionTopic.query.filter_by(question_id=question_id).all()
            # topics = list()
            # for question_topic in question_topics:
            #     topic_id = question_topic.topic_id
            #     topic = Topic.query.filter_by(id=topic_id).first()
            #     topics.append(topic)
            result['topics'] = question.topics
            # lay them thong tin nguoi dung dang upvote hay downvote cau hoi nay
            current_user, _ = AuthController.get_logged_user(request)
            if current_user:
                vote = QuestionVote.query.filter(QuestionVote.user_id == current_user.id, QuestionVote.question_id == question.id).first()
                if vote is not None:
                    result['up_vote'] = True if VotingStatusEnum(2).name == vote.vote_status.name else False
                    result['down_vote'] = True if VotingStatusEnum(3).name == vote.vote_status.name else False
                favorite = QuestionFavorite.query.filter(QuestionFavorite.user_id == current_user.id,
                                                QuestionFavorite.question_id == question.id).first()
                result['is_favorited_by_me'] = True if favorite else False
                # vote = QuestionVote.query.filter(QuestionVote.user_id == current_user.id, QuestionVote.question_id == question.id).first()
                # if vote is not None:
                #     result['up_vote'] = vote.up_vote
                #     result['down_vote'] = vote.down_vote
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

    def create_answer(self, object_id, data):
        if object_id.isdigit():
            question = Question.query.filter_by(id=object_id).first()
        else:
            question = Question.query.filter_by(slug=object_id).first()
        if question is None:
            return send_error(message="Question with ID {} not found".format(object_id))
        
        data['question_id'] = question.id
        if not isinstance(data, dict):
            return send_error(message="Data is not correct or not in dictionary form.")
        if not 'answer' in data:
            return send_error(message='Please fill the answer body before sending.')

        current_user, _ = AuthController.get_logged_user(request)
        if current_user:
            data['user_id'] = current_user.id

        try:
            answer = Answer.query.filter_by(question_id=data['question_id'], user_id=data.get('user_id')).first()
            if answer:
                return send_error(message='This user already answered for this question.')
            # add new answer
            answer = self._parse_answer(data=data, answer=None)
            if answer.answer.__str__().strip().__eq__(''):
                return send_error(message='The answer must include content.')
            is_sensitive = check_sensitive(answer.answer)
            if is_sensitive:
                return send_error(message='Nội dung câu trả lời của bạn không hợp lệ.')
            answer.created_date = datetime.utcnow()
            answer.updated_date = datetime.utcnow()
            answer.last_activity = datetime.utcnow()
            db.session.add(answer)
            db.session.commit()
            result = answer._asdict()
            # khi moi tao thi gia tri up_vote va down_vote cua nguoi dung hien gio la False
            result['up_vote'] = False
            result['down_vote'] = False
            return send_result(message='Answer created successfully', data=marshal(result, AnswerDto.model_response))
        except Exception as e:
            print(e.__str__())
            return send_error(message='Could not create question.')

    def _parse_answer(self, data, answer=None):
        if answer is None:
            answer = Answer()
        # if 'created_date' in data:
        #     try:
        #         answer.created_date = dateutil.parser.isoparse(data['created_date'])
        #         # answer.created_date = dateutil.parser.isoparse(data['created_date'])
        #     except Exception as e:
        #         print(e.__str__())
        #         pass
        # if 'updated_date' in data:
        #     try:
        #         answer.updated_date = dateutil.parser.isoparse(data['updated_date']) #dateutil.parser.isoparse(data['update_date'])
        #     except Exception as e:
        #         print(e.__str__())
        #         pass
        # if 'last_activity' in data:
        #     try:
        #         answer.last_activity = dateutil.parser.isoparse(data['last_activity'])
        #     except Exception as e:
        #         print(e.__str__())
        #         pass
        # if 'upvote_count' in data:
        #     try:
        #         answer.upvote_count = int(data['upvote_count'])
        #     except Exception as e:
        #         print(e.__str__())
        #         pass
        # if 'downvote_count' in data:
        #     try:
        #         answer.downvote_count = int(data['downvote_count'])
        #     except Exception as e:
        #         print(e.__str__())
        #         pass
        if 'anonymous' in data:
            try:
                answer.anonymous = bool(data['anonymous'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'accepted' in data:
            try:
                answer.accepted = bool(data['accepted'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'answer' in data:
            answer.answer = data['answer']
        # if 'markdown' in data:
        #     answer.markdown = data['markdown']
        # if 'html' in data:
        #     answer.html = data['html']
        if 'user_id' in data:
            try:
                answer.user_id = int(data['user_id'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'answer_id' in data:
            try:
                answer.answer_id = int(data['answer_id'])
            except Exception as e:
                print(e.__str__())
                pass
        # if 'image_ids' in data:
        #     try:
        #         answer.image_ids = json.loads(data['image_ids'])
        #     except Exception as e:
        #         print(e.__str__())
        #         pass
            
        if 'is_deleted' in data:
            try:
                answer.is_deleted = bool(data['is_deleted'])
            except Exception as e:
                print(e)
                pass
        if 'user_hidden' in data:
            try:
                answer.user_hidden = bool(data['user_hidden'])
            except Exception as e:
                answer.user_hidden = False
                print(e.__str__())
                pass
        return answer

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
        if 'fixed_topic_name' in data:
            question.fixed_topic_name = data['fixed_topic_name']
        if 'question' in data:
            question.question = data['question']
        if 'accepted_question_id' in data:
            try:
                question.accepted_question_id = int(data['accepted_question_id'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'anonymous' in data:
            try:
                question.anonymous = bool(data['anonymous'])
            except Exception as e:
                print(e.__str__())
                question.anonymous = False
        if 'user_hidden' in data:
            try:
                question.user_hidden = bool(data['user_hidden'])
            except Exception as e:
                question.user_hidden = False
                print(e.__str__())
                pass
        if 'allow_video_question' in data:
            try:
                question.allow_video_question = bool(data['allow_video_question'])
            except Exception as e:
                question.allow_video_question = True
                print(e.__str__())
                pass
        if 'allow_audio_question' in data:
            try:
                question.allow_audio_question = bool(data['allow_audio_question'])
            except Exception as e:
                question.allow_audio_question = True
                print(e.__str__())
                pass
        if 'is_private' in data:
            try:
                question.is_private = bool(data['is_private'])
            except Exception as e:
                question.is_private = False
                print(e.__str__())
                pass
        # if 'image_ids' in data:
        #     try:
        #         question.image_ids = json.loads(data['image_ids'])
        #     except Exception as e:
        #         print(e.__str__())
        #         pass
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
        if 'fixed_topic_name' in data:
            proposal.fixed_topic_name = data['fixed_topic_name']
        if 'question' in data:
            proposal.question = data['question']
        if 'accepted_question_id' in data:
            try:
                proposal.accepted_question_id = int(data['accepted_question_id'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'anonymous' in data:
            try:
                proposal.anonymous = bool(data['anonymous'])
            except Exception as e:
                print(e.__str__())
                proposal.anonymous = False
        if 'user_hidden' in data:
            try:
                proposal.user_hidden = bool(data['user_hidden'])
            except Exception as e:
                proposal.user_hidden = False
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
        if 'is_parma_delete' in data:
            try:
                proposal.is_parma_delete = bool(data['is_parma_delete'])
            except Exception as e:
                proposal.is_parma_delete = False
                print(e.__str__())
                pass
        # if 'image_ids' in data:
        #     try:
        #         proposal.image_ids = json.loads(data['image_ids'])
        #     except Exception as e:
        #         print(e.__str__())
        #         pass
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


    # def get_by_topic_id(self,topic_id):
    #     """ Get all question of a topic that sorted based in upvote count

    #         Args:

    #         Returns:
    #     """

    #     if topic_id is None:
    #         return send_error("Topic ID Không được để trống")

    #     questions = db.session.query(Question).filter(Question.topic_id == topic_id).order_by(desc(Question.upvote_count)).all()

    #     if questions is not None and len(questions) > 0:
    #         results = list()
    #         for question in questions:
    #             # kiem tra den topic
    #             result = question._asdict()
    #             # get user info
    #             user = User.query.filter_by(id=question.user_id).first()
    #             result['user'] = user
    #             # get all topics that question belongs to
    #             question_id = question.id
    #             question_topics = QuestionTopic.query.filter_by(question_id=question_id).all()
    #             topics = list()
    #             for question_topic in question_topics:
    #                 topic_id = question_topic.topic_id
    #                 topic = Topic.query.filter_by(id=topic_id).first()
    #                 topics.append(topic)
    #             result['topics'] = topics
    #             results.append(result)
    #         return send_result(marshal(results, QuestionDto.model_question_response), message='Success')
    #     else:
    #         return send_result(message='Không tìm thấy câu hỏi! ')

    def get_by_slug(self, slug):
        if slug is None:
            return send_error("Question slug is null")
        question = Question.query.filter_by(slug=slug).first()
        if question is None:
            return send_error(message='Could not find question with the slug {}'.format(slug))
        current_user, _ = AuthController.get_logged_user(request)
        if question.is_private:
            if not current_user == question.question_by_user:
                if not self.is_invited(question, current_user):
                    return send_error(message='Question is invitations only.')
        result = question._asdict()
        # get user info
        user = User.query.filter_by(id=question.user_id).first()
        result['user'] = question.question_by_user
        # get all topics that question belongs to
        # question_id = question.id
        # question_topics = QuestionTopic.query.filter_by(question_id=question_id).all()
        # topics = list()
        # for question_topic in question_topics:
        #     topic_id = question_topic.topic_id
        #     topic = Topic.query.filter_by(id=topic_id).first()
        #     topics.append(topic)
        result['topics'] = question.topics
        # lay them thong tin nguoi dung dang upvote hay downvote cau hoi nay
        if current_user:
            vote = QuestionVote.query.filter(QuestionVote.user_id == current_user.id, QuestionVote.question_id == question.id).first()
            if vote is not None:
                result['up_vote'] = True if VotingStatusEnum(2).name == vote.vote_status.name else False
                result['down_vote'] = True if VotingStatusEnum(3).name == vote.vote_status.name else False
            favorite = QuestionFavorite.query.filter(QuestionFavorite.user_id == current_user.id,
                                            QuestionFavorite.question_id == question.id).first()
            result['is_favorited_by_me'] = True if favorite else False
        # vote = QuestionVote.query.filter(QuestionVote.user_id == current_user.id, QuestionVote.question_id == question.id).first()
        # if vote is not None:
        #     result['up_vote'] = vote.up_vote
        #     result['down_vote'] = vote.down_vote
        return send_result(data=marshal(result, QuestionDto.model_question_response), message='Success')

    def update_slug(self):
        questions = Question.query.all()
        try:
            for question in questions:
                question.slug = slugify(question.title)
                db.session.commit()
        except Exception as e:
            print(e.__str__())
            pass
    
    def is_invited(self, question, user):
        if not question.invited_users.contains(user):
            return False
        return True