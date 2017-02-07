from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField
from wtforms.validators import DataRequired


class AddCourseForm(FlaskForm):
    algo = StringField('Algo', validators=[
        DataRequired()
    ])
    otro = StringField('Otro', validators=[
        DataRequired()
    ])
    proofs = FileField('Pruebas')
