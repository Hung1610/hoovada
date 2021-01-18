# third-party modules
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import current_app
from flask_sqlalchemy import SQLAlchemy, SignallingSession
from flask_migrate import Migrate

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class DistributedSession(SignallingSession):
    engines = {}

    def __init__(self, db, autocommit=False, autoflush=True, **options):
        SignallingSession.__init__(self, db, autocommit=False, autoflush=True, **options)
        self.engines = {
            'master': create_engine(self.app.config['SQLALCHEMY_DATABASE_URI']),
            'slave': create_engine(self.app.config['SQLALCHEMY_DATABASE_SLAVE_URI'])
        }

    def get_bind(self, mapper=None, clause=None):
        if self._flushing:
            return self.engines['master']
        return self.engines['slave']


def create_session(self, options):
    return sessionmaker(class_=DistributedSession, db=self, **options)


def get_model(self, name):
    return self.Model._decl_class_registry.get(name, None)


def get_model_by_tablename(self, tablename):
    for c in self.Model._decl_class_registry.values():
        if hasattr(c, '__tablename__') and c.__tablename__ == tablename:
            return c


SQLAlchemy.get_model = get_model
SQLAlchemy.get_model_by_tablename = get_model_by_tablename
SQLAlchemy.create_session = create_session

db = SQLAlchemy()

migrate = Migrate(compare_type=True, compare_server_default=True)