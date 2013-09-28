# -*- coding: utf-8 -*-
"""
    paperchase.frontend.assets
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    frontend application asset "pipeline"
"""

from flask_assets import Environment, Bundle

#: consolidated css bundle
css_all = Bundle("css/PC.css",
                 filters="cssmin", output="css/PC.min.css")

#: application js bundle
js_all = Bundle("js/vendor/angular-cookies.min.js",
                "js/vendor/angular-resource.min.js",
                "js/app.js",
                "js/controllers/controllers.js",
				"js/directives/directives.js",
				"js/services/services.js",
				filters="uglifyjs", output="js/main.min.js")

def init_app(app):
    webassets = Environment(app)
    webassets.register('css_all', css_all)
    webassets.register('js_all', js_all)
    webassets.manifest = 'cache' if not app.debug else False
    webassets.cache = not app.debug
    webassets.debug = app.debug