from flask_restx import Namespace

from app.modules.common.dto import Dto


class UserTopicDto(Dto):
    name = 'user_topic'
    api = Namespace(name)
    model = api.model(name, {

    })
