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
from curpud.tools import get_first_error
from .forms import AddCourseForm
from .models import Course


cour = Blueprint('courses', __name__, url_prefix='/cursos')


@cour.route('/')
def index():
    form = AddCourseForm()
    courses = Course.select()
    return render_template(
        'courses/list.html',
        courses=courses,
        form=form
    )


@cour.route('/profesor/<user>/')
def list(user):
    form = AddCourseForm()
    courses = Course.select().where(Course.owner == user)
    return render_template(
        'courses/list.html',
        courses=courses,
        form=form
    )


@cour.route('/id/<id>/')
def view(doi):
    return render_template('courses/view.html', course="COURSE")


@cour.route('/add/', methods=['POST'])
@flask_login.login_required
def add():
    raise CurpudError("Acción no implementada por completo!")
    user = flask_login.current_user
    form = AddCourseForm()
    if form.validate_on_submit():
        f = form.proofs.data
        filename = secure_filename(user.id + f.filename)
        f.save(os.path.join(
            app.instance_path, 'files', 'courses', filename
        ))
        return redirect(url_for('courses.list', user=user.id))
    else:
        raise CurpudError(get_first_error(form))


@cour.route('/delete/', methods=['POST'])
@flask_login.login_required
def delete():
    raise CurpudError("Acción no implementada!")
    user = flask_login.current_user
    return redirect(url_for('courses.list', user=user.id))
