import peewee as orm
from flask_admin.contrib.peewee import ModelView
from flask import url_for, redirect
import flask_login
import requests

from curpud import db
from curpud.auth.models import User


# Translations
issn_label = 'ISSN'
name_label = 'Nombre'
short_name_label = 'Nombre Corto'
database_label = 'Base de Datos'
web_page_label = 'Página Web'
relevance_label = 'Relevancia'
doi_label = 'DOI'
owner_label = 'Autor'
journal_label = 'Revista'
proofs_file_label = 'Pruebas'


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


class Relevance(BaseModel):
    name = orm.CharField(
        unique=True
    )

    def __str__(self):
        return self.name


class RelevanceView(BaseModelView):
    column_labels = {
        'name': name_label
    }

    form_args = {
        'name': {
            'label': name_label
        }
    }

    column_searchable_list = ['name']


class DataBase(BaseModel):
    name = orm.CharField(
        unique=True
    )
    web_page = orm.TextField(
        null=True
    )
    relevance = orm.ForeignKeyField(
        Relevance,
        related_name='databases'
    )

    def __str__(self):
        return self.name


class DataBaseView(BaseModelView):
    column_labels = {
        'name': name_label,
        'web_page': web_page_label,
        'relevance': relevance_label
    }

    form_args = {
        'name': {
            'label': name_label
        },
        'web_page': {
            'label': web_page_label
        },
        'relevance': {
            'label': relevance_label
        }
    }

    column_searchable_list = ['name', 'web_page', Relevance.name]


class Journal(BaseModel):
    issn = orm.CharField(
        unique=True
    )
    name = orm.CharField(
        unique=True
    )
    short_name = orm.CharField(
        null=True
    )
    sjr = orm.DoubleField(
        null=True
    )
    index = orm.IntegerField(
        null=True
    )
    database = orm.ForeignKeyField(
        DataBase,
        related_name='journals'
    )

    def __str__(self):
        return "{} ({})".format(self.name, self.issn)


class JournalView(BaseModelView):
    column_labels = {
        'issn': issn_label,
        'name': name_label,
        'short_name': short_name_label,
        'database': database_label
    }

    form_args = {
        'issn': {
            'label': issn_label
        },
        'name': {
            'label': name_label
        },
        'short_name': {
            'label': short_name_label
        },
        'database': {
            'label': database_label
        }
    }

    column_searchable_list = ['issn', 'name', 'short_name', DataBase.name]


class Teacher(BaseModel):
    user = orm.ForeignKeyField(User)


class Publication(BaseModel):
    doi = orm.CharField(unique=True)
    owner = orm.CharField()
    journal = orm.ForeignKeyField(Journal)
    proofs_file = orm.CharField(unique=True)

    @property
    def title(self):
        return self._get_json()['message']['title'][0]

    @property
    def indexed_date(self):
        date = self._get_json()['message']['indexed']['date-parts'][0]
        return "/".join(map(str, date))

    @property
    def pages(self):
        return self._get_json()['message']['page']

    @property
    def cites_number(self):
        return self._get_json()['message']['reference-count']

    def _get_json(self):
        url = "http://api.crossref.org/works/{}".format(self.doi)
        r = requests.get(url)
        return r.json()

    def to_dict(self):
        j = self.journal
        return {
            'doi': self.doi,
            'numero_citas': self.cites_number,
            'revista': {
                "nombre": j.name,
                "issn": j.issn,
                "relevancia": j.database.relevance.name,
                "ranking": j.sjr,
                "indexacion": j.index
            }
        }


class PublicationView(BaseModelView):
    column_labels = {
        'doi': doi_label,
        'owner': owner_label,
        'journal': journal_label,
        'proofs_file': proofs_file_label
    }

    form_args = {
        'doi': {
            'label': doi_label
        },
        'owner': {
            'label': owner_label
        },
        'journal': {
            'label': journal_label
        },
        'proofs_file': {
            'label': proofs_file_label
        }
    }

    column_searchable_list = ['doi', 'owner', Journal.name]
