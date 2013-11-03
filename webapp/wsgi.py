from werkzeug.serving import run_simple
from werkzeug.wsgi import DispatcherMiddleware

from paperchase import api, frontend

application = DispatcherMiddleware(frontend.create_app(settings_override = dict(DEBUG = False)), {
            '/api': api.create_app(settings_override = dict(DEBUG = False))
        })