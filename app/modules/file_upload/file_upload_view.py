from flask_restx import Resource
from werkzeug.datastructures import FileStorage

from app.modules.auth.decorator import token_required
from app.modules.file_upload.file_upload_controler import FileUploadController
from app.modules.file_upload.file_upload_dto import FileUploadDto

api = FileUploadDto.api

avatar_upload = api.parser()
avatar_upload.add_argument('image', location='files',
                           type=FileStorage, required=True, help='The image file to upload')


@api.route('/upload_image')
class UploadImage(Resource):
    @token_required
    @api.expect(avatar_upload)
    def post(self):
        '''
        Upload avatar.
        -------------
        :return:
        '''
        args = avatar_upload.parse_args()
        controller = FileUploadController()
        return controller.upload_image(args=args)