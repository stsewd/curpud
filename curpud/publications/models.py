import peewee as orm
from flask_admin.contrib.peewee import ModelView

from curpud import db


# Translations
issn_label = 'ISSN'
name_label = 'Nombre'
short_name_label = 'Nombre Corto'
database_label = 'Base de Datos'
web_page_label = 'Página Web'
relevance_label = 'Relevancia'


class BaseModel(orm.Model):
    class Meta:
        database = db


class BaseModelView(ModelView):
    pass


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
