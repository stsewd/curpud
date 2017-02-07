import click


@click.group()
def cli():
    pass


@cli.command()
def run():
    from curpud import app

    app.run()


@cli.command()
def users():
    create_relevances()
    create_admin_user()
    create_normal_user()


def create_relevances():
    from curpud.publications.models import Relevance
    relevance = Relevance(name="internacional")
    relevance.save()
    relevance = Relevance(name="regional")
    relevance.save()


def create_admin_user():
    from curpud.auth.models import User
    user = User(
        name='Juan',
        lastname='Perez',
        login='admin',
        passwd='21232f297a57a5a743894a0e4a801fc3',  # admin
        is_admin=True
    )
    user.save()


def create_normal_user():
    from curpud.auth.models import User
    user = User(
        name='Marco',
        lastname='Polo',
        login='profe',
        passwd='1145cbf42070c6704b66d6ac75347726'  # profe
    )
    user.save()


if __name__ == "__main__":
    cli()
