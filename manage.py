import click


@click.group()
def cli():
    pass


@cli.command()
def run():
    from curpud import app

    app.run()


if __name__ == "__main__":
    cli()
