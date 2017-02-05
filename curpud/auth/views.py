from hashlib import md5

import flask_login
from flask import (
    Blueprint,
    request,
    render_template,
    redirect,
    url_for,
    abort
)

from .models import User, AuthUser


auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('auth/login.html')

    login = request.form['login']
    pw = request.form['pw']

    try:
        user = User.get(User.login == login)
        if user.passwd == md5(pw.encode()).hexdigest():
            auser = AuthUser()
            auser.id = user.login
            flask_login.login_user(auser)
            return redirect(url_for('index'))
        else:
            raise Exception("Bad login!")
    except:
        return render_template(
            'auth/login.html',
            error="Usuario o contraseña no válidos."
        )


@auth.route('/logout/')
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return redirect(url_for('index'))
