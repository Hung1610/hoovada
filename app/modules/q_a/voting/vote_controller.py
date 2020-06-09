import dateutil.parser
from flask_restx import marshal

from app import db
from app.modules.common.controller import Controller
from app.modules.q_a.voting.vote import Vote
from app.modules.q_a.voting.vote_dto import VoteDto
from app.utils.response import send_error, send_result


class VoteController(Controller):
    def search(self, args):
        '''
        Search votes.

        :param args: The dictionary-like params.

        :return: A list of votes that satisfy conditions.

        '''
        if not isinstance(args, dict):
            return send_error(message='Could not parse params. Check again.')
        user_id, question_id, answer_id, comment_id, from_date, to_date = None, None, None, None, None, None
        if 'user_id' in args:
            try:
                user_id = int(args['user_id'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'question_id' in args:
            try:
                question_id = int(args['question_id'])
            except Exception as e:
                print(e.__str__())
                pass
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
        if user_id is None and question_id is None and answer_id is None and comment_id is None and from_date is None and to_date is None:
            return send_error(message='Please provide params to search.')

        query = db.session.query(Vote)
        is_filter = False
        if user_id is not None:
            query = query.filter(Vote.user_id == user_id)
            is_filter = True
        if question_id is not None:
            query = query.filter(Vote.question_id == question_id)
            is_filter = True
        if answer_id is not None:
            query = query.filter(Vote.answer_id == answer_id)
            is_filter = True
        if comment_id is not None:
            query = query.filter(Vote.comment_id == comment_id)
            is_filter = True
        if from_date is not None:
            query = query.filter(Vote.voting_date >= from_date)
            is_filter = True
        if to_date is not None:
            query = query.filter(Vote.voting_date <= to_date)
            is_filter = True
        if is_filter:
            votes = query.all()
            if votes is not None and len(votes) > 0:
                return send_result(data=marshal(votes, VoteDto.model), message='Success')
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
            return send_result(message='Vote was created successfully.', data=marshal(vote, VoteDto.model))
        except Exception as e:
            print(e.__str__())
            return send_error(message='Could not create vote.')

    def get(self):
        try:
            votes = Vote.query.all()
            return send_result(data=marshal(votes, VoteDto.model), message='Success')
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
            return send_result(data=marshal(vote, VoteDto.model), message='Success')

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
                return send_result(message="Update successfully.", data=marshal(vote, VoteDto.model))

        except Exception as e:
            print(e.__str__())
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
        if 'voting_date' in data:
            try:
                vote.voting_date = dateutil.parser.isoparse(data['voting_date'])
            except Exception as e:
                print(e.__str__())
                pass
        if 'modified_date' in data:
            try:
                vote.modified_date = dateutil.parser.isoparse(data['modified_date'])
            except Exception as e:
                print(e.__str__())
                pass
        return vote
