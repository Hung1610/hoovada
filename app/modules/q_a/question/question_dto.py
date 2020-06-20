from flask_restx import Namespace, fields

from app.modules.common.dto import Dto


class QuestionDto(Dto):
    name = 'question'
    api = Namespace(name)

    model_topic = api.model('topic', {
        'id': fields.Integer(readonly=True, description='The ID of the topic'),
        'name': fields.String(description='The name of the topic'),
        'description': fields.String(description='Description about topic')
    })

    model_question_request = api.model('question_request', {
        'title': fields.String(description='The title of the question'),
        'user_id': fields.Integer(description='The user ID'),
        'fixed_topic_id': fields.Integer(description='The ID of the parent (fixed) topic'),
        'fixed_topic_name': fields.String(description='The name of the parent (fixed) topic'),
        'question': fields.String(description='The content of the question'),
        'accepted_answer_id': fields.Integer(description='The ID of the answer which was accepted'),
        'anonymous': fields.Boolean(default=False, description='The question was created by anonymous'),
        'user_hidden': fields.Boolean(default=False, description='The question wss created by user but the user want to be hidden'),
        'topic_ids': fields.List(fields.Integer, description='The list of topics')  # the list of IDs of topics that question belongs to.
    })

    model_question_response = api.model('question_response', {
        'id': fields.Integer(readonly=True, description=''),
        'title': fields.String(description='The title of the question'),
        'user_id': fields.Integer(description='The user ID'),
        'fixed_topic_id': fields.Integer(description='The ID of the parent (fixed) topic'),
        'fixed_topic_name': fields.String(description='The name of the parent (fixed) topic'),
        'question': fields.String(description='The content of the question'),
        # 'markdown': fields.String(description=''),
        # 'html': fields.String(description=''),
        'created_date': fields.DateTime(description='The created date'),
        'updated_date': fields.DateTime(description='The updated date'),
        'views_count': fields.Integer(default=0, description='The amount of question views'),
        'last_activity': fields.DateTime(description='The last time this question was updated.'),
        'answers_count': fields.Integer(default=0, description='The amount of answers on this question'),
        'accepted_answer_id': fields.Integer(description='The ID of the answer which was accepted'),
        'anonymous': fields.Boolean(default=False, description='The question was created by anonymous'),
        'user_hidden': fields.Boolean(default=False,
                                      description='The question wss created by user but the user want to be hidden'),
        'topics': fields.List(fields.Nested(model_topic), description='The list of topics'),  # the list of IDs of topics that question belongs to.
        'upvote_count': fields.Integer(default=0, description='The amount of upvote'),
        'downvote_count': fields.Integer(default=0, description='The amount of downvote'),
        'share_count': fields.Integer(default=0, description='The amount of sharing'),
        'favorite_count': fields.Integer(default=0, description='The amount of favorite')
        # 'image_ids':fields.String()
    })
