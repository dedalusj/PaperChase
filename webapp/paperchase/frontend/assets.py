# -*- coding: utf-8 -*-
"""
    paperchase.frontend.assets
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    frontend application asset "pipeline"
"""

from flask_assets import Environment, Bundle
from ..helpers import assetsList

main_js_filename = "main.min.js"

def init_app(app):
    webassets = Environment(app)
    
    css_all = Bundle("css/PC.css", filters="cssmin", output="css/PC.min.css")
    webassets.register('css_all', css_all)
    
    js_list = assetsList(app, exclusions = [main_js_filename])
    js_all = Bundle(*js_list, filters="uglifyjs", output="js/main.min.js")
    webassets.register('js_all', js_all)
    
    webassets.manifest = 'cache' if not app.debug else False
    webassets.cache = not app.debug
    webassets.debug = app.debug