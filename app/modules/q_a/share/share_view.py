from flask_restx import Resource
# from app.modules.common.decorator import token_required
from .share_dto import ShareDto
from .share_controller import ShareController
from ...auth.decorator import admin_token_required, token_required

api = ShareDto.api
share = ShareDto.model


@api.route('')
class ShareList(Resource):
    @admin_token_required
    @api.marshal_list_with(share)
    def get(self):
        '''
        Get list of shares from database.

        :return: The list of shares.
        '''
        controller = ShareController()
        return controller.get()

    @token_required
    @api.expect(share)
    @api.marshal_with(share)
    def post(self):
        '''
        Create new share.

        :return: The new share if it was created successfully and null vice versa.
        '''
        data = api.payload
        controller = ShareController()
        return controller.create(data=data)


@api.route('/<int:share_id>')
class Share(Resource):
    @token_required
    @api.marshal_with(share)
    def get(self, share_id):
        '''
        Get share by its ID.

        :param share_id: The ID of the share.

        :return: The share with the specific ID.
        '''
        controller = ShareController()
        return controller.get_by_id(object_id=share_id)

    @token_required
    @api.expect(share)
    @api.marshal_with(share)
    def put(self, share_id):
        '''
        Update existing share by its ID.

        :param share_id: The ID of the share which need to be updated.

        :return: The updated share if success and null vice versa.
        '''
        data = api.payload
        controller = ShareController()
        return controller.update(object_id=share_id, data=data)

    @token_required
    def delete(self, share_id):
        '''
        Delete share by its ID.

        :param share_id: The ID of the share.

        :return:
        '''
        controller = ShareController()
        return controller.delete(object_id=share_id)
