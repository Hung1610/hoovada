from flask_restx import fields, Namespace

from app.modules.common.dto import Dto


class ReportDto(Dto):
    name = 'report'
    api = Namespace(name)
    model_request = api.model('report_quest', {
        'user_id': fields.Integer(description=''),
        'question_id': fields.Integer(description=''),
        'answer_id': fields.Integer(description=''),
        'comment_id': fields.Integer(description=''),
        'inappropriate': fields.Boolean(description=''),
        'description': fields.String(description='')
    })

    model_response = api.model('report_response', {
        'id': fields.Integer(description=''),
        'user_id': fields.Integer(description=''),
        'question_id': fields.Integer(description=''),
        'answer_id': fields.Integer(description=''),
        'comment_id': fields.Integer(description=''),
        'inappropriate': fields.Boolean(description=''),
        'description': fields.String(description=''),
        'created_date': fields.DateTime(description='')
    })
