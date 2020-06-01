from flask_restx import Namespace, fields

from app.modules.common.dto import Dto


# class SignupUserDto(Dto):
#     name = 'signup_user'
#     api = Namespace(name)
#     model = api.model(name, {
#         'id': fields.Integer(),
#         'email': fields.String(required=True),
#         'password': fields.String(required=True),
#         'registered_date': fields.Date(),
#         'registered_time': fields.DateTime(),
#         'activation_code': fields.String(),
#         'code_created_date': fields.Date(),
#         'code_created_time': fields.DateTime(),
#         'code_duration_time': fields.Float(),
#         'code_sent_date': fields.Date(),
#         'code_sent_time': fields.DateTime(),
#         'trial_number': fields.Integer(),
#         'confirm': fields.Boolean()
#     })


# class RecoveryUserDto(Dto):
#     name = 'recovery_user'
#     api = Namespace(name)
#     model = api.model(name, {
#         'id': fields.Integer(),
#         'email': fields.String(),
#         'new_password': fields.String(),
#         'required_date': fields.Date(),
#         'required_time': fields.DateTime(),
#         'recovery_code': fields.String(),
#         'code_created_date': fields.Date(),
#         'code_created_time': fields.DateTime(),
#         'code_duration_time': fields.Float(),
#         'code_sent_date': fields.Date(),
#         'code_sent_time': fields.DateTime(),
#         'trial_number': fields.Integer(),
#         'continued': fields.Boolean(),
#         'session_start_date': fields.Date(),
#         'session_start_time': fields.DateTime(),
#         'session_duration': fields.Float(),
#         'recovered': fields.Boolean()
#     })


class UserDto(Dto):
    name = 'user'
    api = Namespace(name)
    model = api.model(name, {
        'id': fields.Integer(readonly=True),
        'display_name': fields.String(),
        'title': fields.String(),

        'first_name': fields.String(),
        'middle_name': fields.String(),
        'last_name': fields.String(),

        'gender': fields.String(),
        'age': fields.String(),
        'email': fields.String(),
        'password': fields.String(),

        'last_seen': fields.DateTime(),
        'joined_date': fields.DateTime(),
        'confirmed': fields.Boolean(),
        'email_confirmed_at': fields.DateTime(),

        'profile_pic_url': fields.String(),
        'profile_pic_data_url': fields.String(),
        'admin': fields.Boolean(),
        'active': fields.Boolean(),

        'reputation': fields.Integer(),
        'profile_views': fields.Integer(),
        'city': fields.String(),
        'country': fields.String(),
        'website_url': fields.String(),

        'about_me': fields.String(),
        'about_me_markdown': fields.String(),
        'about_me_html': fields.String(),

        'people_reached': fields.Integer(),
        'job_role': fields.String(),
        'company': fields.String(),

        'show_email_publicly_setting': fields.Boolean(),
        'hoovada_digests_setting': fields.Boolean(),
        'hoovada_digests_frequency_setting': fields.String(),

        'questions_you_asked_or_followed_setting': fields.Boolean(),
        'questions_you_asked_or_followed_frequency_setting': fields.String(),
        'people_you_follow_setting': fields.Boolean(),
        'people_you_follow_frequency_setting': fields.String(),

        'email_stories_topics_setting': fields.Boolean(),
        'email_stories_topics_frequency_setting': fields.String(),
        'last_message_read_time': fields.DateTime()
    })
