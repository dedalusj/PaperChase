# -*- coding: utf-8 -*-
"""
    paperchase.frontend.assets
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    frontend application asset "pipeline"
"""

from flask_assets import Environment, Bundle

#: application css bundle
#css_paperchase = Bundle("less/PC.less",
#                       filters="less", output="css/paperchase.css",
#                       debug=False)

#: consolidated css bundle
css_all = Bundle("css/PC.css",
                 "css/bootstrap.css",
                 "css/bootstrap-theme.css",
                 filters="cssmin", output="css/PC.min.css")

#: vendor js bundle
js_vendor = Bundle("js/vendor/jquery-1.10.1.min.js",
                   "js/vendor/angular.min.js",
                   "js/vendor/angular-resource.min.js",
                   "js/vendor/base64.js",
                   "js/vendor/bootstrap.js",
                   filters="jsmin", output="js/vendor.min.js")

#: application js bundle
js_main = Bundle("js/main/main.js",
				 "js/main/controllers/mainController.js",
				 output="js/main.js")

def init_app(app):
    webassets = Environment(app)
    webassets.register('css_all', css_all)
    webassets.register('js_vendor', js_vendor)
    webassets.register('js_main', js_main)
    webassets.manifest = 'cache' if not app.debug else False
    webassets.cache = not app.debug
    webassets.debug = app.debug