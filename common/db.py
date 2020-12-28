# third-party modules
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."
    

def get_model(self, name):
    return self.Model._decl_class_registry.get(name, None)


def get_model_by_tablename(self, tablename):
    for c in self.Model._decl_class_registry.values():
        if hasattr(c, '__tablename__') and c.__tablename__ == tablename:
            return c


SQLAlchemy.get_model = get_model
SQLAlchemy.get_model_by_tablename = get_model_by_tablename
db = SQLAlchemy()

migrate = Migrate(compare_type=True, compare_server_default=True)