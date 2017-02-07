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
from .models import Course, TypeCourse


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
    courses = Course.select().where(Course.assistent == user)
    return render_template(
        'courses/list.html',
        courses=courses,
        form=form
    )


@cour.route('/id/<id>/')
def view(id):
    try:
        course = Course.get(Course.id == id)
    except:
        abort(404)
    else:
        return render_template('courses/view.html',
                               course=course)


@cour.route('/add/', methods=['POST'])
@flask_login.login_required
def add():
    user = flask_login.current_user
    form = AddCourseForm()
    if form.validate_on_submit():
        f = form.proofs.data
        filename = secure_filename(user.id + f.filename)
        f.save(os.path.join(
            app.instance_path, 'files', 'courses', filename
        ))

        Course.create(
            assistent = user.id,
            name=form.name.data,
            place = form.place.data,
            type = TypeCourse.get(form.type.data == TypeCourse.id),
            init_date = form.init_date.data,
            end_date = form.end_date.data,
            proofs_file = filename
        )
        return redirect(url_for('courses.list', user=user.id))
    else:
        raise CurpudError(get_first_error(form))


@cour.route('/delete/', methods=['POST'])
@flask_login.login_required
def delete():
    raise CurpudError("Acción no implementada!")
    user = flask_login.current_user
    return redirect(url_for('courses.list', user=user.id))
