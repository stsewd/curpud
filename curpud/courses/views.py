from flask import (
    Blueprint,
    redirect,
    url_for,
    abort
)


cour = Blueprint('courses', __name__, url_prefix='/cursos')


@cour.route('/')
def index():
    return "Cursos"
