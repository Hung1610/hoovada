from datetime import datetime
from elasticsearch_dsl import Document, Date, Integer, Keyword, Text, analyzer, tokenizer, char_filter
from elasticsearch_dsl.connections import connections

class User(Document):
    id = Integer()
    display_name = Text(analyzer='standard', fields={'raw': Keyword()})
    email = Text(analyzer='standard', fields={'raw': Keyword()})
    gender = Text(fields={'raw': Keyword()})
    age = Integer()
    last_name = Text(analyzer='standard', fields={'raw': Keyword()})
    first_name = Text(analyzer='standard', fields={'raw': Keyword()})
    middle_name = Text(analyzer='standard', fields={'raw': Keyword()})
    reputation = Integer()

    class Index:
        name = "user"
        settings = {"number_of_shards": 1, "number_of_replicas": 0}
