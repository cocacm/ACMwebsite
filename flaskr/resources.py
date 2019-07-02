from flask import (
    Blueprint, render_template
)

bp = Blueprint('resources', __name__,url_prefix='/resources')

@bp.route('/')
def resources():
    return render_template('resources/resources.html')

@bp.route('/coding-practice')
def practice():
    return render_template('resources/coding-practice.html')

@bp.route('/learning')
def learning():
    return render_template('resources/learning.html')
