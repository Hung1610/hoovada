from elasticsearch_dsl import connections
from common.models.es.user import User
from common.models.es.post import Post
from common.models.es.article import Article
from common.models.es.question import Question
from common.models.es.topic import Topic
from app.settings.config import BaseConfig as Config

connections.create_connection(hosts=[Config.ES_HOST], timeout=Config.ES_TIMEOUT)


def get_model(name):
    mapping = {
        'User': User,
        'Post': Post,
        'Article': Article,
        'Question': Question,
        'Topic': Topic
    }
    return mapping[name]