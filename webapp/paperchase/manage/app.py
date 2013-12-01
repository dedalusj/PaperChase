from flask.ext.script import Command, Option

from .. import api


class Run(Command):

    """Run the server in debug mode"""

    option_list = (
        Option('--host', '-o', dest='host', default='localhost'),
        Option('--port', '-p', dest='port', default=5000),
    )

    def run(self, host, port):
        application = api.create_app()
        application.run(host=host, port=port, debug=True,
                        use_reloader=True, use_debugger=True)
