import os

from werkzeug.utils import secure_filename
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
from curpud import app
from .forms import AddPublicationForm
from curpud.tools import get_first_error
from .models import Journal, Publication


pub = Blueprint('publications', __name__, url_prefix='/publicaciones')


@pub.route('/')
def index():
    form = AddPublicationForm()
    publications = Publication.select()
    return render_template(
        'publications/list.html',
        publications=publications,
        form=form
    )


@pub.route('/profesor/<user>/')
def list(user):
    form = AddPublicationForm()
    publications = Publication.select().where(Publication.owner == user)
    return render_template(
        'publications/list.html',
        publications=publications,
        form=form
    )


@pub.route('/doi/<path:doi>/')
def view(doi):
    return render_template('publications/view.html', publication="PUBLICACION")


@pub.route('/add/', methods=['POST'])
@flask_login.login_required
def add():
    user = flask_login.current_user
    form = AddPublicationForm()
    if form.validate_on_submit():
        f = form.proofs.data
        filename = secure_filename(user.id + f.filename)
        f.save(os.path.join(
            app.instance_path, 'files', 'publications', filename
        ))
        # TODO: revisar que el doi pertenezca a una revista
        Publication.create(
            doi=form.doi.data,
            proofs_file=filename,
            owner=user.id,
            journal=Journal.get(Journal.issn == form.issn.data)
        )
        return redirect(url_for('publications.list', user=user.id))
    else:
        raise CurpudError(get_first_error(form))


@pub.route('/delete/', methods=['POST'])
@flask_login.login_required
def delete():
    raise CurpudError("Acción no implementada!")
    user = flask_login.current_user
    return redirect(url_for('publications.list', user=user.id))
