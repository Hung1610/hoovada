from datetime import datetime
from elasticsearch_dsl import Document, Date, Integer, Keyword, Text, analyzer, tokenizer, Index
from elasticsearch_dsl.connections import connections
from common.utils.custom_analyzer import vn_text_analyzer

user_friend_index = Index('user_friend')
@user_friend_index.document
class UserFriend(Document):
    friend_id = Integer()
    friended_id = Integer()
    friend_display_name = Text(analyzer='standard')
    friend_email = Text(analyzer='standard')
    friend_profile_pic_url = Text()
    friended_display_name = Text(analyzer='standard')
    friended_email = Text(analyzer='standard')
    friended_profile_pic_url = Text()
    is_approved = Integer()