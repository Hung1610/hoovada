from flask_restx import Namespace

from app.modules.common.dto import Dto


class QuestionDto(Dto):
    name = 'question'
    api = Namespace(name)
    model = api.model(name, {
        'question_d'
    })
