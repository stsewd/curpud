import flask_login
from flask import (
    Blueprint,
    redirect,
    url_for,
    abort,
    request,
    render_template
)

from curpud import CurpudError
from .forms import AddPublicationForm


pub = Blueprint('publications', __name__, url_prefix='/publicaciones')


@pub.route('/')
def index():
    form = AddPublicationForm()
    return render_template(
        'publications/list.html',
        publications=[],
        form=form
    )


@pub.route('/profesor/<user>/')
def list(user):
    form = AddPublicationForm()
    return render_template(
        'publications/list.html',
        publications=[],
        form=form
    )


@pub.route('/doi/<doi>/')
def view(doi):
    return render_template('publications/view.html', publication="PUBLICACION")


@pub.route('/add/', methods=['POST'])
@flask_login.login_required
def add():
    raise CurpudError("Acción no implementada!")
    user = flask_login.current_user
    return redirect(url_for('publications.list', user=user.id))


@pub.route('/delete/', methods=['POST'])
@flask_login.login_required
def delete():
    raise CurpudError("Acción no implementada!")
    user = flask_login.current_user
    return redirect(url_for('publications.list', user=user.id))
