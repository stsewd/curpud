from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class AddPublicationForm(FlaskForm):
    issn = StringField('ISSN de la Revista', validators=[
        DataRequired()
    ])
    doi_or_name = StringField('DOI o Nombre de la Publicación', validators=[
        DataRequired()
    ])
