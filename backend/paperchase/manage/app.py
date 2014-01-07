from flask.ext.script import Command, Option

from ..helpers import reverseproxied
from .. import api


class Run(Command):

    """Run the server in debug mode"""

    option_list = (
        Option('--host', '-o', dest='host', default='localhost'),
        Option('--port', '-p', dest='port', default=5000),
    )

    def run(self, host, port):
        app = api.create_app()
        app.wsgi_app = reverseproxied.ReverseProxied(app.wsgi_app)
        app.run(host=host, port=port, debug=True, use_debugger=False)
