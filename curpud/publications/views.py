from flask import (
    Blueprint,
    redirect,
    url_for,
    abort
)


pub = Blueprint('publications', __name__, url_prefix='/publicaciones')


@pub.route('/')
def index():
    return "Publicaciones"
