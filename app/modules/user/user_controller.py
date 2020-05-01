from app.utils.response import send_result
from app.modules.common.controller import Controller


class UserController(Controller):
    def create(self, data):
        pass

    def get(self):
        return send_result("List of users has sent")

    def get_by_id(self, object_id):
        pass

    def update(self, object_id, data):
        pass

    def delete(self, object_id):
        pass
