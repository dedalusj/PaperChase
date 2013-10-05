from flask.ext.script import Command, Option

from werkzeug.serving import run_simple
from werkzeug.wsgi import DispatcherMiddleware

from .. import api, frontend

class RunDebug(Command):
    """Run the server in debug mode"""
    
    option_list = (
            Option('--host', '-o', dest='host', default='0.0.0.0'),
            Option('--port', '-p', dest='port', default=5000),
    )
    
    def run(self, host, port):
        application = DispatcherMiddleware(frontend.create_app(), {'/api': api.create_app()})
        run_simple(host, port, application, use_reloader=True, use_debugger=True)

class RunApp(RunDebug):
    """Run the server in development mode"""
    
    def run(self, host, port):
        application = DispatcherMiddleware(frontend.create_app(settings_override = dict(DEBUG = False)), {
            '/api': api.create_app(settings_override = dict(DEBUG = False))
        })
        run_simple(host, port, application, use_reloader=True, use_debugger=False)