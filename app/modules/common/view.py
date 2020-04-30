from flask_restplus import Resource as BaseResource
# from app.modules.common.decorator import admin_token_required, token_required
from abc import ABC, abstractmethod


class Resource(BaseResource):
    """
    Abstract class from which all view classes will inherit.
    """

    @abstractmethod
    def get(self):
        pass

    @abstractmethod
    def post(self):
        pass


class ResourceId(BaseResource):
    @abstractmethod
    def get(self, object_id):
        pass

    @abstractmethod
    def put(self, object_id, data):
        pass

    @abstractmethod
    def delete(self, object_id):
        pass
