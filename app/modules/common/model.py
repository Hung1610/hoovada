from abc import ABC, abstractmethod
from app.app import db


class Model(db.Model):
    """
    Class entity is parent class for all other class
    """
    __abstract__ = True
