import typer

from scout.api import hello

app = typer.Typer(no_args_is_help=True)


@app.callback()
def callback():
    """
    Scout
    """


@app.command()
def test():
    """
    Load the scout
    """
    typer.echo(hello())
