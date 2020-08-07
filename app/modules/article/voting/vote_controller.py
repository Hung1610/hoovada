#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

# third-party modules
import dateutil.parser
from flask_restx import marshal

# own modules
from app import db
from app.modules.common.controller import Controller
from app.modules.q_a.answer.answer import Answer
from app.modules.q_a.comment.comment import Comment
from app.modules.q_a.question.question import Question
from app.modules.q_a.voting.vote import Vote
from app.modules.q_a.voting.vote_dto import VoteDto
from app.modules.user.user import User
from app.utils.response import send_error, send_result

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

class VoteController(Controller):
    def search(self, args):
        '''
        Search votes.

        :param args: The dictionary-like params.

        :return: A list of votes that satisfy conditions.

        '''
        if not isinstance(args, dict):
            return send_error(message='Could not parse params. Check again.')
        user_id, answer_id, comment_id, from_date, to_date = None, None, None, None, None
        if 'user_id' in args:
            try:
                user_id = int(args['user_id'])
            except Exception as e:
                print(e.__str__())
                pass
        # if 'question_id' in args:
        #     try:
        #         question_id = int(args['question_id'])
        #     except Exception as e:
        #         print(e.__str__())
        #         pass
        if 'answer_id' in args:
            try:
                answer_id = int(args['answer_id'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'comment_id' in args:
            try:
                comment_id = int(args['comment_id'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'from_date' in args:
            try:
                from_date = dateutil.parser.isoparse(args['from_date'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'to_date' in args:
            try:
                to_date = dateutil.parser.isoparse(args['to_date'])
            except Exception as e:
                print(e.__str__())
                pass
        if user_id is None and answer_id is None and comment_id is None and from_date is None and to_date is None:
            return send_error(message='Please provide params to search.')
        query = db.session.query(Vote)
        is_filter = False
        if user_id is not None:
            query = query.filter(Vote.user_id == user_id)
            is_filter = True
        # if question_id is not None:
        #     query = query.filter(Vote.question_id == question_id)
        #     is_filter = True
        if answer_id is not None:
            query = query.filter(Vote.answer_id == answer_id)
            is_filter = True
        if comment_id is not None:
            query = query.filter(Vote.comment_id == comment_id)
            is_filter = True
        if from_date is not None:
            query = query.filter(Vote.created_date >= from_date)
            is_filter = True
        if to_date is not None:
            query = query.filter(Vote.created_date <= to_date)
            is_filter = True
        if is_filter:
            votes = query.all()
            if votes is not None and len(votes) > 0:
                return send_result(data=marshal(votes, VoteDto.model_response), message='Success')
            else:
                return send_result(message='Could not find any votes.')
        else:
            return send_error(message='Could not find votes. Please check your parameters again.')

    def create(self, data):
        if not isinstance(data, dict):
            return send_error(message='Data is not correct or not in dictionary form. Please fill params.')
        if not 'user_id' in data:
            return send_error(message='User ID must be included.')
        try:
            vote = self._parse_vote(data=data, vote=None)
            db.session.add(vote)
            db.session.commit()
            return send_result(message='Vote was created successfully.', data=marshal(vote, VoteDto.model_response))
        except Exception as e:
            print(e.__str__())
            return send_error(message='Could not create vote.')

    def create_question_vote(self, data):
        if not isinstance(data, dict):
            return send_error(message='Data is not correct or not in dictionary form. Please fill params.')
        if not 'user_id' in data:
            return send_error(message='User ID must be included.')
        if not 'question_id' in data:
            return send_error(message='the `question_id` must be included.')
        try:
            # add vote
            # if 'comment_id' in data:
            #     return send_error(
            #         message='This API only supports answer vote. Please use comment API instead for voting comment.')
            vote = self._parse_vote(data=data, vote=None)
            if vote.up_vote == vote.down_vote:
                return send_error(message='User can only upvote or downvote at one time.')
            vote.created_date = datetime.utcnow()
            vote.updated_date = datetime.utcnow()
            db.session.add(vote)
            db.session.commit()
            # update answer vote count in answer and user
            try:
                
                question = Question.query.filter_by(id=vote.question_id).first()
                # user who votes
                user = User.query.filter_by(id=vote.user_id).first()
                # get user who was created answer and was voted
                user_voted = User.query.filter_by(id=question.user_id).first()
                if vote.up_vote:
                    question.upvote_count += 1
                    user.question_upvote_count += 1
                    user_voted.answer_upvoted_count += 1
                elif vote.down_vote:
                    question.downvote_count += 1
                    user.question_downvote_count += 1
                    user_voted.question_downvoted_count += 1
                db.session.commit()
                return send_result(data=marshal(vote, VoteDto.model_response), message='Success')
            except Exception as e:
                print(e.__str__())
                pass
        except Exception as e:
            print(e.__str__())
            return send_error(message='Could not add vote. Error {}'.format(e.__str__()))

    def create_answer_vote(self, data):
        if not isinstance(data, dict):
            return send_error(message='Data is not correct or not in dictionary form. Please fill params.')
        if not 'user_id' in data:
            return send_error(message='User ID must be included.')
        if not 'answer_id' in data:
            return send_error(message='the `answer_id` must be included.')
        try:
            # add vote
            # if 'comment_id' in data:
            #     return send_error(
            #         message='This API only supports answer vote. Please use comment API instead for voting comment.')
            vote = self._parse_vote(data=data, vote=None)
            if vote.up_vote == vote.down_vote:
                return send_error(message='User can only upvote or downvote at one time.')
            vote.created_date = datetime.utcnow()
            vote.updated_date = datetime.utcnow()
            db.session.add(vote)
            db.session.commit()
            # update answer vote count in answer and user
            try:
                answer = Answer.query.filter_by(id=vote.answer_id).first()
                # user who votes
                user = User.query.filter_by(id=vote.user_id).first()
                # get user who was created answer and was voted
                user_voted = User.query.filter_by(id=answer.user_id).first()
                if vote.up_vote:
                    answer.upvote_count += 1
                    user.answer_upvote_count += 1
                    user_voted.answer_upvoted_count += 1
                elif vote.down_vote:
                    answer.downvote_count += 1
                    user.answer_downvote_count += 1
                    user_voted.answer_downvoted_count += 1
                db.session.commit()
                return send_result(data=marshal(vote, VoteDto.model_response), message='Success')
            except Exception as e:
                print(e.__str__())
                pass
        except Exception as e:
            print(e.__str__())
            return send_error(message='Could not add vote. Error {}'.format(e.__str__()))

    def create_comment_vote(self, data):
        if not isinstance(data, dict):
            return send_error(message='Data is not correct or not in dictionary form. Please fill params.')
        if not 'user_id' in data:
            return send_error(message='User ID must be included.')
        if not 'comment_id' in data:
            return send_error(message='The `comment_id` must be included.')
        try:
            # add vote
            # if 'answer_id' in data:
            #     return send_error(
            #         message='This API only supports comment vote. Please use answer API instead for voting answer.')
            vote = self._parse_vote(data=data, vote=None)
            if vote.up_vote == vote.down_vote:
                return send_error(message='User can only upvote or downvote at one time.')
            db.session.add(vote)
            db.session.commit()
            # update comment vote count in answer and user
            try:
                comment = Comment.query.filter_by(id=vote.comment_id).first()
                # user who votes
                user = User.query.filter_by(id=vote.user_id).first()
                # get user who was created comment and was voted
                user_voted = User.query.filter_by(id=comment.user_id).first()
                if vote.up_vote:
                    comment.upvote_count += 1
                    user.comment_upvote_count += 1
                    user_voted.comment_upvoted_count += 1
                if vote.down_vote:
                    comment.downvote_count += 1
                    user.comment_downvote_count += 1
                    user_voted.comment_downvoted_count += 1
                db.session.commit()
                return send_result(data=marshal(vote, VoteDto.model_response), message='Success')
            except Exception as e:
                print(e.__str__())
                pass
        except Exception as e:
            print(e.__str__())
            return send_error(message='Could not add vote. Error {}'.format(e.__str__()))

    def get(self):
        try:
            votes = Vote.query.all()
            return send_result(data=marshal(votes, VoteDto.model_response), message='Success')
        except Exception as e:
            print(e.__str__())
            return send_error(message='Could not load votes.')

    def get_by_id(self, object_id):
        if object_id is None:
            return send_error(message='Vote ID is null.')
        vote = Vote.query.filter_by(id=object_id).first()
        if vote is None:
            return send_error(message='Could not find vote with ID {}.'.format(object_id))
        else:
            return send_result(data=marshal(vote, VoteDto.model_response), message='Success')

    def update(self, object_id, data):
        if object_id is None:
            return send_error(message='Vote ID is null.')
        if data is None or not isinstance(data, dict):
            return send_error(message='Data is null or not in dictionary form. Check again.')
        try:
            vote = Vote.query.filter_by(id=object_id).first()
            if vote is None:
                return send_error(message='Vote with the ID {} not found.'.format(object_id))
            else:
                vote = self._parse_vote(data=data, vote=vote)
                db.session.commit()
                return send_result(message="Update successfully.", data=marshal(vote, VoteDto.model_response))

        except Exception as e:
            print(e.__str__())
            return send_error(message='Could not update vote.')

    def update_question_vote(self, object_id, data):
        if object_id is None:
            return send_error(message='Vote ID is null.')
        if data is None or not isinstance(data, dict):
            return send_error(message='Data is null or not in dictionary form. Check again.')
        if not 'user_id' in data:
            return send_error(message='User ID must be included.')
        # check user_id if
        if not 'question_id' in data:
            return send_error(message='the `question_id` must be included.')
        try:
            vote = Vote.query.filter_by(id=object_id).first()
            if not vote:
                return send_error(message='The vote with the ID {} does not exist.'.format(object_id))
            vote_parse = self._parse_vote(data=data, vote=None)
            if vote_parse.up_vote == vote_parse.down_vote:
                return send_error(message='Up-vote and down-vote can not be the same at the same time.')
            if vote_parse.up_vote == vote.up_vote and vote_parse.down_vote == vote.down_vote:
                return send_result(message='The values of upvote and downvote have not changed.')
            # get question
            question = Question.query.filter_by(id=vote.question_id).first()
            # get user who voted
            user = User.query.filter_by(id=vote.user_id).first()
            # get user whose question has been voted
            # get user whose question has been upvoted
            user_voted = User.query.filter_by(id=question.user_id).first()
            if vote_parse.up_vote:  # if user change vote from down_vote to up_vote
                # update downvote_count cho question
                question.downvote_count -= 1
                # update question_downvote_count cho user
                user.question_downvote_count -= 1
                # update question_downvoted_count cho user
                user_voted.question_downvoted_count -= 1

                ## for upvote
                # update upvote_count cho question
                question.upvote_count += 1
                # update question_upvote_count cho user
                user.question_upvote_count += 1
                # update question_upvoted_count cho user
                user_voted.question_upvoted_count += 1

                # update up_vote and down_vote cho vote
                vote.up_vote = True
                vote.down_vote = False
            if vote_parse.down_vote:
                # update upvote_count cho question
                question.upvote_count -= 1
                # Update question_upvote_count cho user
                user.question_upvote_count -= 1
                # Update question_upvoted_count cho user
                user_voted.question_upvoted_count -= 1

                # Update downvote_count cho question
                question.downvote_count += 1
                # Update question_downvote_count cho user
                user.question_downvote_count += 1
                # Update question_downvoted_count cho user
                user_voted.question_downvoted_count += 1

                # Update up_vote và down_vote cho vote
                vote.up_vote = False
                vote.down_vote = True
            # Lưu lại dữ liệu
            db.session.commit()
        except Exception as e:
            print(e.__str__())
            db.session.rollback()
            return send_error(message='Could not update vote. Try again later.')

    def update_answer_vote(self, object_id, data):
        if object_id is None:
            return send_error(message='Vote ID is null.')
        if data is None or not isinstance(data, dict):
            return send_error(message='Data is null or not in dictionary form. Check again.')
        if not 'user_id' in data:
            return send_error(message='User ID must be included.')
        # check user_id if
        if not 'answer_id' in data:
            return send_error(message='the `answer_id` must be included.')
        try:
            vote = Vote.query.filter_by(id=object_id).first()
            if not vote:
                return send_error(message='The vote with the ID {} does not exist.'.format(object_id))
            vote_parse = self._parse_vote(data=data, vote=None)
            if vote_parse.up_vote == vote_parse.down_vote:
                return send_error(message='Up-vote and down-vote can not be the same at the same time.')
            if vote_parse.up_vote == vote.up_vote and vote_parse.down_vote == vote.down_vote:
                return send_result(message='The values of upvote and downvote have not changed.')
            # get answer
            answer = Answer.query.filter_by(id=vote.answer_id).first()
            # get user who voted
            user = User.query.filter_by(id=vote.user_id).first()
            # get user whose question has been voted
            # get user whose answer has been upvoted
            user_voted = User.query.filter_by(id=answer.user_id).first()
            if vote_parse.up_vote:  # if user change vote from down_vote to up_vote
                # update downvote_count cho answer
                answer.downvote_count -= 1
                # update answer_downvote_count cho user
                user.answer_downvote_count -= 1
                # update answer_downvoted_count cho user
                user_voted.answer_downvoted_count -= 1

                ## for upvote
                # update upvote_count cho answer
                answer.upvote_count += 1
                # update answer_upvote_count cho user
                user.answer_upvote_count += 1
                # update answer_upvoted_count cho user
                user_voted.answer_upvoted_count += 1

                # update up_vote and down_vote cho vote
                vote.up_vote = True
                vote.down_vote = False
            if vote_parse.down_vote:
                # update upvote_count cho answer
                answer.upvote_count -= 1
                # Update answer_upvote_count cho user
                user.answer_upvote_count -= 1
                # Update answer_upvoted_count cho user
                user_voted.answer_upvoted_count -= 1

                # Update downvote_count cho answer
                answer.downvote_count += 1
                # Update answer_downvote_count cho user
                user.answer_downvote_count += 1
                # Update answer_downvoted_count cho user
                user_voted.answer_downvoted_count += 1

                # Update up_vote và down_vote cho vote
                vote.up_vote = False
                vote.down_vote = True
            # Lưu lại dữ liệu
            db.session.commit()
        except Exception as e:
            print(e.__str__())
            db.session.rollback()
            return send_error(message='Could not update vote. Try again later.')

    def update_comment_vote(self, object_id, data):
        if object_id is None:
            return send_error(message='Vote ID is null.')
        if data is None or not isinstance(data, dict):
            return send_error(message='Data is null or not in dictionary form. Check again.')
        if not 'user_id' in data:
            return send_error(message='User ID must be included.')
        if not 'comment_id' in data:
            return send_error(message='The `comment_id` must be included.')
        try:
            # check vote
            vote = Vote.query.filter_by(id=object_id).first()
            if not vote:
                return send_error(message='The vote with the ID {} does not exist.'.format(object_id))
            vote_parse = self._parse_vote(data=data, vote=None)
            if vote_parse.up_vote == vote_parse.down_vote:
                return send_error(message='Up-vote and down-vote can not be the same at the same time.')
            if vote_parse.up_vote == vote.up_vote and vote_parse.down_vote == vote.down_vote:
                return send_result(message='The values of upvote and downvote have not changed.')
            # get the comment
            comment = Comment.query.filter_by(id=vote.comment_id).first()
            # get the user who voted
            user = User.query.filter_by(id=vote.user_id).first()
            # get the user whose comment voted
            user_voted = User.query.filter_by(id=comment.user_id).first()
            if vote_parse.up_vote:
                # Update downvote_count cho table comment
                comment.downvote_count -= 1
                # Update comment_downvote_count cho table user
                user.comment_downvote_count -= 1
                # Update comment_downvoted_count cho table user
                user_voted.comment_downvoted_count -= 1

                # Update upvote_count cho table comment
                comment.upvote_count += 1
                # Update comment_upvote_count cho table user
                user.comment_upvote_count += 1
                # Update comment_upvoted_count cho table user
                user_voted.comment_upvoted_count += 1
                # Update up_vote và down_vote cho vote
                vote.up_vote = True
                vote.down_vote = False

            if vote_parse.down_vote:
                # Update upvote_count cho table comment
                comment.upvote_count -= 1
                # Update comment_upvote_count cho table user
                user.comment_upvote_count -= 1
                # Update comment_upvoted_count cho table user
                user_voted.comment_upvoted_count -= 1

                # Update downvote_count cho table comment
                comment.downvote_count += 1
                # Update comment_downvote_count cho table user
                user.comment_downvote_count += 1
                # Update comment_downvoted_count cho table user
                user_voted.comment_downvoted_count += 1

                # Update up_vote và down_vote cho vote
                vote.up_vote = False
                vote.down_vote = True
            # Lưu lại dữ liệu
            db.session.commit()
        except Exception as e:
            print(e.__str__())
            db.session.rollback()
            return send_error(message='Could not update vote.')

    def delete(self, object_id):
        if object_id is None:
            return send_error(message='ID must be included to delete.')
        try:
            vote = Vote.query.filter_by(id=object_id).first()
            if vote is None:
                return send_error(message='Vote with ID {} not found.'.format(object_id))
            else:
                db.session.delete(vote)
                db.session.commit()
                return send_result(message='Vote with the ID {} was deleted.'.format(object_id))
        except Exception as e:
            print(e.__str__())
            return send_error(message='Could not delete vote with ID {}.'.format(object_id))

    def delete_question_vote(self, object_id):
        if object_id is None:
            return send_error(message='ID must be included to delete.')
        try:
            vote = Vote.query.filter_by(id=object_id).first()
            if vote is None:
                return send_error(message='Vote with ID {} not found.'.format(object_id))
            else:
                # lay ra question
                question = Question.query.filter_by(id=vote.question_id).first()
                # lay ra user who voted
                user = User.query.filter_by(id=vote.user_id).first()
                # lay ra user whose question has been voted
                user_voted = User.query.filter_by(id=question.user_id).first()
                if vote.up_vote:
                    # Cập nhật upvote_count cho question
                    question.upvote_count -= 1
                    # Cập nhật question_upvote_count cho user
                    user.question_upvote_count -= 1
                    # Cập nhật question_upvoted_count cho user
                    user_voted.question_upvoted_count -= 1
                if vote.down_vote:
                    # Cập nhật downvote_count cho question
                    question.downvote_count -= 1
                    # Cập nhật question_downvote_count cho user
                    user.question_downvote_count -= 1
                    # Cập nhật question_downvoted_count cho user
                    user_voted.question_downvoted_count -= 1
                # commit change to db first
                db.session.commit()
                # delete vote
                db.session.delete(vote)
                db.session.commit()
                return send_result(message='Vote with the ID {} was deleted.'.format(object_id))
        except Exception as e:
            print(e.__str__())
            return send_error(message='Could not delete vote with ID {}.'.format(object_id))

    def delete_answer_vote(self, object_id):
        if object_id is None:
            return send_error(message='ID must be included to delete.')
        try:
            vote = Vote.query.filter_by(id=object_id).first()
            if vote is None:
                return send_error(message='Vote with ID {} not found.'.format(object_id))
            else:
                # lay ra answer
                answer = Answer.query.filter_by(id=vote.answer_id).first()
                # lay ra user who voted
                user = User.query.filter_by(id=vote.user_id).first()
                # lay ra user whose answer has been voted
                user_voted = User.query.filter_by(id=answer.user_id).first()
                if vote.up_vote:
                    # Cập nhật upvote_count cho answer
                    answer.upvote_count -= 1
                    # Cập nhật answer_upvote_count cho user
                    user.answer_upvote_count -= 1
                    # Cập nhật answer_upvoted_count cho user
                    user_voted.answer_upvoted_count -= 1
                if vote.down_vote:
                    # Cập nhật downvote_count cho answer
                    answer.downvote_count -= 1
                    # Cập nhật answer_downvote_count cho user
                    user.answer_downvote_count -= 1
                    # Cập nhật answer_downvoted_count cho user
                    user_voted.answer_downvoted_count -= 1
                # commit change to db first
                db.session.commit()
                # delete vote
                db.session.delete(vote)
                db.session.commit()
                return send_result(message='Vote with the ID {} was deleted.'.format(object_id))
        except Exception as e:
            print(e.__str__())
            return send_error(message='Could not delete vote with ID {}.'.format(object_id))

    def delete_comment_vote(self, object_id):
        if object_id is None:
            return send_error(message='ID must be included to delete.')
        try:
            vote = Vote.query.filter_by(id=object_id).first()
            if vote is None:
                return send_error(message='Vote with ID {} not found.'.format(object_id))
            else:
                # lay ra comment
                comment = Comment.query.filter_by(id=vote.comment_id).first()
                # lay ra user
                user = User.query.filter_by(id=vote.user_id).first()
                # lay ra user_voted
                user_voted = User.query.filter_by(id=comment.user_id).first()
                if vote.up_vote:
                    # Cập nhật upvote_count cho comment
                    comment.upvote_count -= 1
                    # Cập nhật comment_upvote_count cho user
                    user.comment_upvote_count -= 1
                    # Cập nhật comment_upvoted_count cho user
                    user_voted.comment_upvoted_count -= 1
                if vote.down_vote:
                    # Cập nhật downvote_count cho comment
                    comment.downvote_count -= 1
                    # Cập nhật comment_downvote_count cho user
                    user.comment_downvote_count -= 1
                    # Cập nhật comment_downvoted_count cho user
                    user_voted.comment_downvoted_count -= 1
                # commit changes to db first
                db.session.commit()
                # delete vote
                db.session.delete(vote)
                db.session.commit()
                return send_result(message='Vote with the ID {} was deleted.'.format(object_id))
        except Exception as e:
            print(e.__str__())
            db.session.rollback()
            return send_error(message='Could not delete vote with ID {}'.format(object_id))

    def _parse_vote(self, data, vote=None):
        if vote is None:
            vote = Vote()
        if 'user_id' in data:
            try:
                vote.user_id = int(data['user_id'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'question_id' in data:
             try:
                 vote.question_id = int(data['question_id'])
             except Exception as e:
                 print(e.__str__())
                 pass
        if 'answer_id' in data:
            try:
                vote.answer_id = int(data['answer_id'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'comment_id' in data:
            try:
                vote.comment_id = int(data['comment_id'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'up_vote' in data:
            try:
                vote.up_vote = bool(data['up_vote'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'down_vote' in data:
            try:
                vote.down_vote = bool(data['down_vote'])
            except Exception as e:
                print(e.__str__())
                pass
        # if 'voting_date' in data:
        #     try:
        #         vote.voting_date = dateutil.parser.isoparse(data['voting_date'])
        #     except Exception as e:
        #         print(e.__str__())
        #         pass
        # if 'modified_date' in data:
        #     try:
        #         vote.modified_date = dateutil.parser.isoparse(data['modified_date'])
        #     except Exception as e:
        #         print(e.__str__())
        #         pass
        return vote
