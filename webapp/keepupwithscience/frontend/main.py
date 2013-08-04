from flask import Blueprint, render_template

#from . import route

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """Returns the main interface."""
    return render_template('main.html')