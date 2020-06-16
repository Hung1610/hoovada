from flask_restx import Namespace, fields

from app.modules.common.dto import Dto


class QuestionDto(Dto):
    name = 'question'
    api = Namespace(name)

    model_topic = api.model('topic', {
        'id': fields.Integer(readonly=True),
        'name': fields.String(),
        'description': fields.String()
    })

    model_question_request = api.model('question_request', {
        'title': fields.String(),
        'user_id': fields.Integer(),
        'fixed_topic_id': fields.Integer(),
        'fixed_topic_name': fields.String(),
        'question': fields.String(),  # use just question for storing the question body
        # 'markdown': fields.String(),
        # 'html': fields.String(),
        # 'created_date': fields.DateTime(),
        # 'updated_date': fields.DateTime(),
        # 'views': fields.Integer(),
        # 'last_activity': fields.DateTime(),
        # 'answers_count': fields.Integer(),
        'accepted_answer_id': fields.Integer(),
        'anonymous': fields.Boolean(default=False),
        'user_hidden': fields.Boolean(default=False),
        # 'image_ids': fields.String()
        'topic_ids': fields.List(fields.Integer)  # the list of IDs of topics that question belongs to.
    })

    model_question_response = api.model('question_response', {
        'id': fields.Integer(readonly=True),
        'title': fields.String(),
        'user_id': fields.Integer(),
        'fixed_topic_id': fields.Integer(),
        'fixed_topic_name': fields.String(),  # the name of the fixed topic
        'question': fields.String(),
        # 'markdown': fields.String(),
        # 'html': fields.String(),
        'created_date': fields.DateTime(),
        'updated_date': fields.DateTime(),
        'views_count': fields.Integer(default=0),
        'last_activity': fields.DateTime(),
        'answers_count': fields.Integer(default=0),
        'accepted_answer_id': fields.Integer(),
        'anonymous': fields.Boolean(default=False),
        'user_hidden': fields.Boolean(default=False),
        'topics': fields.List(fields.Nested(model_topic)),  # the topics that question belongs to.
        'upvote_count': fields.Integer(default=0),
        'downvote_count': fields.Integer(default=0),
        'share_count': fields.Integer(default=0),
        'favorite_count': fields.Integer(default=0)
        # 'image_ids':fields.String()
    })
