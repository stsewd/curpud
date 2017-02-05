from flask import (
    Blueprint,
    request,
    render_template,
    redirect,
    url_for,
    abort
)


auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.route('/signin/')
def signin():
    return "Redireccionar..."
