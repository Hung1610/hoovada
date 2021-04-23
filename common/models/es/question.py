from datetime import datetime
from elasticsearch_dsl import Document, Date, Integer, Keyword, Text, analyzer, tokenizer, char_filter
from elasticsearch_dsl.connections import connections
from common.utils.custom_analyzer import vn_html_analyzer, vn_text_analyzer

class Question(Document):
    id = Integer()
    question = Text(analyzer='standard')
    title = Text(analyzer='standard', fields={'raw': Keyword()})
    user_id = Integer()
    slug = Text(analyzer='standard', fields={'raw': Keyword()})
    created_date = Date()
    updated_date = Date()

    class Index:
        name = "question"
        settings = {"number_of_shards": 1, "number_of_replicas": 0}