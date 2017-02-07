import peewee as orm
import flask_login

from curpud import db


class BaseModel(orm.Model):
    class Meta:
        database = db


class User(BaseModel):
    name = orm.CharField()
    lastname = orm.CharField()
    login = orm.CharField(unique=True)
    passwd = orm.CharField()
    is_admin = orm.BooleanField(default=False)


class AuthUser(flask_login.UserMixin):

    @property
    def is_admin(self):
        user = User.get(User.login == self.id)
        return user.is_admin

