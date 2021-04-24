from datetime import datetime
from elasticsearch_dsl import Document, Date, Integer, Keyword, Text, analyzer, tokenizer, Index
from elasticsearch_dsl.connections import connections
from common.utils.custom_analyzer import vn_text_analyzer

article_index = Index('article')
@article_index.document
class Question(Document):
    id = Integer()
    question = Text(analyzer=vn_text_analyzer)
    title = Text(analyzer=vn_text_analyzer, fields={'raw': Keyword()})
    user_id = Integer()
    slug = Text(analyzer='standard', fields={'raw': Keyword()})
    created_date = Date()
    updated_date = Date()