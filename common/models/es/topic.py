from datetime import datetime
from elasticsearch_dsl import Document, Date, Integer, Keyword, Text, analyzer, tokenizer, char_filter
from elasticsearch_dsl.connections import connections
from common.utils.custom_analyzer import vn_html_analyzer, vn_text_analyzer

class Topic(Document):
    id = Integer()
    html = Text(analyzer='standard')
    user_id = Integer()
    created_date = Date()
    updated_date = Date()

    class Index:
        name = "topic"
        settings = {"number_of_shards": 1, "number_of_replicas": 0}