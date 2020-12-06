from common.scheduled_jobs import scheduler
from app.apis import init_api
from app.app import init_app


def create_app():
    app = init_app()
    # Config Restful APIs
    api = init_api()
    api.init_app(app)
    # Config ApScheduler
    scheduler.init_app(app)
    scheduler.start()

    return app