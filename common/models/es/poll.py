from datetime import datetime
from elasticsearch_dsl import Document, Date, Integer, Keyword, Text, analyzer, tokenizer, Index
from elasticsearch_dsl.connections import connections
from common.utils.custom_analyzer import vn_text_analyzer

poll_index = Index('poll')
@poll_index.document
class Poll(Document):
    id = Integer()
    title = Text(analyzer='standard')
    user_id = Integer()
    created_date = Date()
    updated_date = Date()