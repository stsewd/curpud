from flask import Flask, render_template, redirect, url_for


app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')

app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


@app.route('/')
def index():
    return redirect(url_for('publications.index'))


from .auth.views import auth
from .publications.views import pub

app.register_blueprint(auth)
app.register_blueprint(pub)
