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
    create_courses_types()
    create_admin_user()
    create_normal_user()
    populate_databases()
    populate_journals_regional()


def create_relevances():
    from curpud.publications.models import Relevance
    relevance = Relevance(name="internacional")
    relevance.save()
    relevance = Relevance(name="regional")
    relevance.save()


def create_courses_types():
    from curpud.courses.models import TypeCourse
    tc = TypeCourse(name="seminario")
    tc.save()
    tc = TypeCourse(name="mooc")
    tc.save()
    tc = TypeCourse(name="capacitación")
    tc.save()


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


def populate_databases():
    from curpud.publications.models import DataBase, Relevance
    DataBase.create(
        name='ebsco',
        relevance=Relevance.get(Relevance.name == 'regional')
    )
    DataBase.create(
        name='esmerald',
        relevance=Relevance.get(Relevance.name == 'regional')
    )
    DataBase.create(
        name='web of knowledge',
        relevance=Relevance.get(Relevance.name == 'internacional')
    )
    DataBase.create(
        name='scopus',
        relevance=Relevance.get(Relevance.name == 'internacional')
    )


def populate_journals_regional():
    import csv
    from curpud.publications.models import Journal, DataBase
    base_path = 'scripts/output/'
    for filename, database in [('ebsco.csv', 'ebsco'), ('emerald.csv', 'esmerald')]:
        with open(base_path + filename) as csvfile:
            csv_reader = csv.reader(csvfile)
            next(csv_reader)  # Headers
            for row in csv_reader:
                short_name, long_name, issn = row
                try:
                    Journal.create(
                        name=long_name,
                        short_name=short_name,
                        issn=issn,
                        database=DataBase.get(DataBase.name == database)
                    )
                except:
                    continue


if __name__ == "__main__":
    cli()
