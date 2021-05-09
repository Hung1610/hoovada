from datetime import datetime
from elasticsearch_dsl import Document, Date, Integer, Keyword, Text, analyzer, tokenizer, Index
from elasticsearch_dsl.connections import connections
from common.utils.custom_analyzer import vn_text_analyzer


post_index = Index('post')
@post_index.document
class Post(Document):
    id = Integer()
    html = Text(analyzer=vn_text_analyzer)
    user_id = Integer()
    created_date = Date()
    updated_date = Date()