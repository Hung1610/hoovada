from datetime import datetime
from elasticsearch_dsl import Document, Date, Integer, Keyword, Text, analyzer, tokenizer, char_filter, Index
from elasticsearch_dsl.connections import connections
from common.utils.custom_analyzer import vn_text_analyzer

topic_index = Index('topic')
@topic_index.document
class Topic(Document):
    id = Integer()
    description = Text(analyzer=vn_text_analyzer)
    name = Text(analyzer=vn_text_analyzer)
    slug= Text(analyzer='standard')
    is_fixed = Integer()
    user_id = Integer()
    created_date = Date()
    updated_date = Date()