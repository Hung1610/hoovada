from flask_restx import Resource, reqparse
# from app.modules.common.decorator import token_required
from .user_topic_dto import UserTopicDto
from .user_topic_controller import UserTopicController
from app.modules.auth.decorator import admin_token_required, token_required

api = UserTopicDto.api
user_topic = UserTopicDto.model


@api.route('')
class UserTopicList(Resource):
    @admin_token_required
    # @api.marshal_list_with(user_topic)
    @api.response(code=200, model=user_topic, description='Model for question topic response.')
    def get(self):
        '''
        Get list of user_topics from database.

        :return: The list of user_topics.
        '''
        controller = UserTopicController()
        return controller.get()

    @token_required
    @api.expect(user_topic)
    # @api.marshal_with(user_topic)
    @api.response(code=200, model=user_topic, description='Model for question topic response.')
    def post(self):
        '''
        Create new user_topic.

        :return: The new user_topic if it was created successfully and null vice versa.
        '''
        data = api.payload
        controller = UserTopicController()
        return controller.create(data=data)


@api.route('/<int:id>')
class UserTopic(Resource):
    @token_required
    # @api.marshal_with(user_topic)
    @api.response(code=200, model=user_topic, description='Model for question topic response.')
    def get(self, id):
        '''
        Get user_topic by its ID.

        :param id: The ID of the user_topic.

        :return: The user_topic with the specific ID.
        '''
        controller = UserTopicController()
        return controller.get_by_id(object_id=id)

    @token_required
    @api.expect(user_topic)
    # @api.marshal_with(user_topic)
    @api.response(code=200, model=user_topic, description='Model for question topic response.')
    def put(self, id):
        '''
        Update existing user_topic by its ID.

        :param id: The ID of the user_topic which need to be updated.

        :return: The updated user_topic if success and null vice versa.
        '''
        data = api.payload
        controller = UserTopicController()
        return controller.update(object_id=id, data=data)

    @token_required
    def delete(self, id):
        '''
        Delete user_topic by its ID.

        :param id: The ID of the user_topic.

        :return:
        '''
        controller = UserTopicController()
        return controller.delete(object_id=id)


parser = reqparse.RequestParser()
parser.add_argument('user_id', type=str, required=False, help='Search record by user ID.')
parser.add_argument('topic_id', type=str, required=False, help='Search records by topic ID.')


@api.route('/search')
@api.expect(parser)
class UserTopicSearch(Resource):
    @token_required
    @api.response(code=200, model=user_topic, description='Model for question topic response.')
    def get(self):
        """
        Search all topics that satisfy conditions.
        ---------------------

        :user_id: Search topic by user_id (who created topics)

        :parent_id: Search all topics by their parent topic ID.

        :return: List of buyers
        """
        args = parser.parse_args()
        controller = UserTopicController()
        return controller.search(args=args)
