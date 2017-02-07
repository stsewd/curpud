from hashlib import md5
from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    abort,
    jsonify,
    g
)
import flask_login
import flask_admin
import peewee as orm


# App global configuration
app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')


# jinja template configuration
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True


# Database global configuration
db = orm.MySQLDatabase(
    'curpud',
    host=app.config['DB_HOST'],
    user=app.config['DB_USER'],
    passwd=app.config['DB_PASSWD']
)

from .publications.models import (
    Relevance, RelevanceView,
    DataBase, DataBaseView,
    Journal, JournalView,
    Publication, PublicationView
)
from .auth.models import User, AuthUser

try:
    db.connect()
    db.create_tables([User])
    db.create_tables([Relevance, DataBase, Journal])
    db.create_tables([Publication])
except Exception as e:
    pass


# Admin panel configurations
admin = flask_admin.Admin(
    app, name='curpud',
    base_template='custom_admin/master.html',
    template_mode='bootstrap3'
)
admin.add_views(
    RelevanceView(Relevance, 'Categorías'),
    DataBaseView(DataBase, 'Bases de Datos'),
    JournalView(Journal, 'Revistas'),
    PublicationView(Publication, 'Publicaciones')
)


# Authentication configuration
login_manager = flask_login.LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def user_loader(login):
    try:
        user = User.get(User.login == login)
        auser = AuthUser()
        auser.id = user.login
        return auser
    except:
        return


@login_manager.request_loader
def request_loader(request):
    login = request.form.get('login')
    try:
        user = User.get(User.login == login)
        auser = AuthUser()
        auser.id = user.login

        passwd = md5(request.form['pw'].encode()).hexdigest()
        auser.is_authenticated = passwd == user.passwd
        return auser
    except:
        return


@login_manager.unauthorized_handler
def unauthorized_handler():
    abort(404)


@app.before_request
def before_request():
    g.db = db
    g.db.connect()


@app.after_request
def after_request(response):
    g.db.close()
    return response


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


# Custom errors
class CurpudError(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)
        self.msg = msg

    def to_dict(self):
        return {
            'description': self.msg,
            'status': 'error'
        }


@app.errorhandler(CurpudError)
def fbcm_error_handler(error):
    response = jsonify(error.to_dict())
    return response


@app.route('/')
def index():
    return redirect(url_for('publications.index'))


from .auth.views import auth
from .courses.views import cour
from .publications.views import pub

app.register_blueprint(auth)
app.register_blueprint(cour)
app.register_blueprint(pub)
