from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, SelectField, DateField
from wtforms.validators import DataRequired

from .models import TypeCourse


class AddCourseForm(FlaskForm):
    name = StringField('Tema', validators=[
        DataRequired()
    ])
    place = StringField('Lugar', validators=[
        DataRequired()
    ])
    type = SelectField(
        'Tipo',
        validators=[
            DataRequired(message="Tipo faltante")
        ],
        coerce=int
    )
    init_date = DateField('Fecha de Inicio', validators=[
        DataRequired()
    ])
    end_date = DateField('Fecha de Fin', validators=[
        DataRequired()
    ])

    proofs = FileField('Pruebas')

    def __init__(self):
        FlaskForm.__init__(self)
        self.type.choices = [
            (t.id, t.name)
            for t in TypeCourse.select().order_by(
                TypeCourse.name
            )
        ]
