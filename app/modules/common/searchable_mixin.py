
class SearchableMixin(object):

    @classmethod
    def search(cls, query, page_number, per_page):
        # ids, total = query_index(cls.__tablename__, query, page_number, per_page)
        pass

    @classmethod
    def before_commit(cls, session):
        pass

    @classmethod
    def after_commit(cls, session):
        pass



