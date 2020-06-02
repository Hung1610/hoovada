from flask_restx import Namespace, fields

from app.modules.common.dto import Dto


class SignupUserDto(Dto):
    name = 'signup_user'
    api = Namespace(name)
    model = api.model(name, {
        'id': fields.Integer(),
        'email': fields.String(required=True),
        'password': fields.String(required=True),
        'registered_date': fields.Date(),
        'registered_time': fields.DateTime(),
        'activation_code': fields.String(),
        'code_created_date': fields.Date(),
        'code_created_time': fields.DateTime(),
        'code_duration_time': fields.Float(),
        'code_sent_date': fields.Date(),
        'code_sent_time': fields.DateTime(),
        'trial_number': fields.Integer(),
        'confirm': fields.Boolean()
    })


class RecoveryUserDto(Dto):
    name = 'recovery_user'
    api = Namespace(name)
    model = api.model(name, {
        'id': fields.Integer(),
        'email': fields.String(),
        'new_password': fields.String(),
        'required_date': fields.Date(),
        'required_time': fields.DateTime(),
        'recovery_code': fields.String(),
        'code_created_date': fields.Date(),
        'code_created_time': fields.DateTime(),
        'code_duration_time': fields.Float(),
        'code_sent_date': fields.Date(),
        'code_sent_time': fields.DateTime(),
        'trial_number': fields.Integer(),
        'continued': fields.Boolean(),
        'session_start_date': fields.Date(),
        'session_start_time': fields.DateTime(),
        'session_duration': fields.Float(),
        'recovered': fields.Boolean()
    })


class UserDto(Dto):
    name = 'user'
    api = Namespace(name)
    model = api.model(name, {
        'id': fields.Integer(readonly=True),
        'display_name': fields.String(required=False),
        'title': fields.String(required=False),

        'first_name': fields.String(required=False),
        'middle_name': fields.String(required=False),
        'last_name': fields.String(required=False),

        'gender': fields.String(required=False),
        'age': fields.String(required=False),
        'email': fields.String(required=False),
        'password': fields.String(required=False),

        'last_seen': fields.DateTime(required=False),
        'joined_date': fields.DateTime(required=False),
        'confirmed': fields.Boolean(required=False),
        'email_confirmed_at': fields.DateTime(required=False),

        'profile_pic_url': fields.String(required=False),
        'profile_pic_data_url': fields.String(required=False),
        'admin': fields.Boolean(required=False),
        'active': fields.Boolean(required=False),

        'reputation': fields.Integer(required=False),
        'profile_views': fields.Integer(required=False, readonly=True),
        'city': fields.String(required=False),
        'country': fields.String(required=False),
        'website_url': fields.String(required=False),

        'about_me': fields.String(required=False),
        'about_me_markdown': fields.String(required=False),
        'about_me_html': fields.String(required=False),

        'people_reached': fields.Integer(required=False),
        'job_role': fields.String(required=False),
        'company': fields.String(required=False),

        'show_email_publicly_setting': fields.Boolean(required=False),
        'hoovada_digests_setting': fields.Boolean(required=False),
        'hoovada_digests_frequency_setting': fields.String(required=False),

        'questions_you_asked_or_followed_setting': fields.Boolean(required=False),
        'questions_you_asked_or_followed_frequency_setting': fields.String(required=False),
        'people_you_follow_setting': fields.Boolean(required=False),
        'people_you_follow_frequency_setting': fields.String(required=False),

        'email_stories_topics_setting': fields.Boolean(required=False),
        'email_stories_topics_frequency_setting': fields.String(required=False),
        'last_message_read_time': fields.DateTime(required=False)
    })
