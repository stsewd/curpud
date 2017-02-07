import peewee as orm
from flask_admin.contrib.peewee import ModelView
from flask import url_for, redirect
import flask_login

from curpud import db
from curpud.auth.models import User


# Translations
place_label = 'Lugar'
name_label = 'Nombre'
type_label = 'Tipo'
proofs_file_label = 'Pruebas'
assistent_label = 'Asistente'
init_date_label = 'Fecha de Inicio'
end_date_label = 'Fecha de Fin'


class BaseModel(orm.Model):
    class Meta:
        database = db


class BaseModelView(ModelView):
    can_export = True
    details_modal = True

    def is_accessible(self):
        auser = flask_login.current_user
        if auser.is_anonymous:
            return False
        user = User.get(User.login == auser.id)
        return auser.is_authenticated and user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('auth.login'))


class TypeCourse(BaseModel):
    name = orm.CharField(
        unique=True
    )

    def __str__(self):
        return self.name


class TypeCourseView(BaseModelView):
    column_labels = {
        'name': name_label
    }

    form_args = {
        'name': {
            'label': name_label
        }
    }

    column_searchable_list = ['name']


class Course(BaseModel):
    name = orm.CharField(
        unique=True
    )
    assistent = orm.CharField()
    place = orm.TextField()
    type = orm.ForeignKeyField(
        TypeCourse,
        related_name='courses'
    )
    init_date = orm.DateField()
    end_date = orm.DateField()
    proofs_file = orm.CharField(unique=True)

    def __str__(self):
        return "{} {}".format(self.name, self.place)


class CourseView(BaseModelView):
    column_labels = {
        'name': name_label,
        'assistent': assistent_label,
        'place': place_label,
        'type': type_label,
        'init_date': init_date_label,
        'end_date': end_date_label,
        'proofs_file': proofs_file_label
    }

    form_args = {
        'name': {
            'label': name_label
        },
        'assistent': {
            'label': assistent_label
        },
        'place': {
            'label': place_label
        },
        'type': {
            'label': type_label
        },
        'init_date': {
            'label': init_date_label
        },
        'end_date': {
            'label': end_date_label
        },
        'proofs_file': {
            'label': proofs_file_label
        }
    }

    column_searchable_list = ['name', 'assistent', 'place', TypeCourse.name]
