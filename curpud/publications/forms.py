from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField
from wtforms.validators import DataRequired


class AddPublicationForm(FlaskForm):
    issn = StringField('ISSN de la Revista', validators=[
        DataRequired()
    ])
    doi = StringField('DOI de la Publicación', validators=[
        DataRequired()
    ])
    proofs = FileField('Pruebas')
