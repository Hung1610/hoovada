# from common.scheduled_jobs import scheduler
import dramatiq
from app.dramatiq_consumers import dramatiq as app_dramatiq
from app.apis import init_api
from app.app import init_app


def create_app():
    app = init_app()
    # Config Restful APIs
    api = init_api()
    api.init_app(app)
    # Config Dramatiq
    app_dramatiq.init_app(app)
    broker = app_dramatiq.broker
    worker = dramatiq.Worker(broker)
    worker.start()

    return app

flask_app = create_app()