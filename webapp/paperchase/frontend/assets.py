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
    """
    Initialise the assets for the :class:`Flask` app
    """
    webassets = Environment(app)
    
    webassets.manifest = 'cache' if not app.debug else False
    webassets.cache = not app.debug
    webassets.debug = app.debug    
    webassets.config['LESS_BIN'] = 'less'
    
    # style sheets
    css_all = Bundle(
        'css/PC.less',
        filters='less,cssmin',
        extra={'rel': 'stylesheet/less' if webassets.debug else 'stylesheet'},
        output='css/PC.min.css'
    )
    webassets.register('css_all', css_all)
    
    webassets.config['less_run_in_debug'] = False
    
    # javascripts
    js_list = assetsList(app, exclusions = [main_js_filename, 'less-1.4.1.min.js'])
    js_all = Bundle(*js_list, filters="uglifyjs", output="js/main.min.js")
    webassets.register('js_all', js_all)
    
    if webassets.debug:
        js_all.contents += tuple(['js/vendor/less-1.4.1.min.js'])