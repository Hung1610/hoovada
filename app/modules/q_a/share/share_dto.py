from flask_restx import fields

from app.modules.common.dto import Dto
from flask_restx_patched import Namespace


class ShareDto(Dto):
    name = 'share'
    api = Namespace(name)
    model = api.model(name, {

    })