import peewee as orm

from curpud import db


class BaseModel(orm.Model):
    class Meta:
        database = db


class Relevance(BaseModel):
    name = orm.CharField(unique=True)


class DataBase(BaseModel):
    name = orm.CharField(unique=True)
    web_page = orm.TextField(null=True)
    relevance = orm.ForeignKeyField(Relevance, related_name='databases')


class Jounal(BaseModel):
    issn = orm.CharField(unique=True)
    name = orm.CharField(unique=True)
    short_name = orm.CharField(null=True)
    database = orm.ForeignKeyField(DataBase, related_name='journals')
