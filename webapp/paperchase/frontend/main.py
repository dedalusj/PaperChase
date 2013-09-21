from flask import Blueprint, render_template, make_response

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """Returns the main interface."""
    return make_response(open('paperchase/frontend/templates/main.html').read())
#    return render_template('main.html')