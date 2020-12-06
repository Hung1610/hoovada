
# own modules
from app.app import init_basic_app
from app.dramatiq_consumers import dramatiq


def create_app():
    app = init_basic_app()
    dramatiq.init_app(app)
    return app

create_app()
broker = dramatiq.broker
