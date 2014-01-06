from werkzeug.serving import run_simple
from werkzeug.wsgi import DispatcherMiddleware

from flask import Flask
from flask.ext.script import Command, Option

from .. import api


class Run(Command):

    """Run the server in debug mode"""

    option_list = (
        Option('--host', '-o', dest='host', default='localhost'),
        Option('--port', '-p', dest='port', default=5000),
    )

    def run(self, host, port):
        application = DispatcherMiddleware(
            Flask('dummy_app'), {'/api': api.create_app()})
        run_simple(host, port, application,
                   use_reloader=True, use_debugger=False)
