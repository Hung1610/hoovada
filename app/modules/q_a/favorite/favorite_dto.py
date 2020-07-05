from flask_restx import fields, Namespace

from app.modules.common.dto import Dto


class FavoriteDto(Dto):
    name = 'favorite'
    api = Namespace(name)

    model_request = api.model('favorite_request', {
        'user_id': fields.Integer(required=True, description='The user ID who favorited'),
        'favorited_user_id': fields.Integer(required=False, description='The user ID who has been favorited'),
        'question_id': fields.Integer(required=False, description='The question ID which has been favorited'),
        'answer_id': fields.Integer(required=False, description='The answer ID which has been favorited'),
        'comment_id': fields.Integer(required=False, description='The comment ID which has been favorited')
    })

    model_response = api.model('favorite_response', {
        'id': fields.Integer(required=False, readonly=True, description='The ID of the record'),
        'user_id': fields.Integer(required=True, description='The user ID who favorited'),
        'favorited_user_id': fields.Integer(required=False, description='The user ID who has been favorited'),
        'question_id': fields.Integer(required=False, description='The question ID which has been favorited'),
        'answer_id': fields.Integer(required=False, description='The answer ID which has been favorited'),
        'comment_id': fields.Integer(required=False, description='The comment ID which has been favorited'),
        'created_date': fields.DateTime(required=False, description='The created date'),
        'updated_date': fields.DateTime(required=False, description='The updated date')
    })
