from flask_restx import Namespace, fields

from app.modules.common.dto import Dto


class CommentDto(Dto):
    name = 'comment'
    api = Namespace(name)
    model_requesst = api.model('comment_request', {
        'comment': fields.String(required=True, description='The content of the comment'),
        # 'question_id': fields.Integer(required=False),
        'answer_id': fields.Integer(required=True, description='The ID of the answer'),
        'user_id': fields.Integer(required=True, description='The user ID')
    })

    model_response = api.model('comment_response', {
        'id': fields.Integer(required=False, readonly=True, description='The ID of the comment'),
        'comment': fields.String(required=True, description='The content of the comment'),
        'created_date': fields.DateTime(required=True, description='The date comment was created'),
        # 'question_id': fields.Integer(),
        'answer_id': fields.Integer(required=True, description='The ID of the answer'),
        'user_id': fields.Integer(required=True, description='The user ID'),
        'updated_date': fields.DateTime(description='The date comment was updated'),
        'upvote_count': fields.Integer(description='The amount of upvote'),
        'downvote_count': fields.Integer(description='The amount of downvote'),
        'report_count': fields.Integer(description='The amount of report')
    })
