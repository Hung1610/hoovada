from flask_restx import fields

from app.modules.common.dto import Dto
from flask_restx_patched import Namespace


class VoteDto(Dto):
    name = 'vote'
    api = Namespace(name)
    model = api.model(name, {

    })
