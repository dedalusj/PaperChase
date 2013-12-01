from paperchase import api

application = api.create_app(settings_override=dict(DEBUG=False))
