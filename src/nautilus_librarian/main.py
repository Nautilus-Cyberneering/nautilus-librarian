"""
    Main Module for Librarian
    Usage: main.py [OPTIONS] COMMAND [ARGS]...

    Commands:
      process  Execute the image processing pipeline.
      pull     Retrieves the images from the DVC remote storage.

    Current implementation is just a boilerplate to add logic, now only prints info through console.
"""

import nautilus_librarian.dvc
import nautilus_librarian.git
import nautilus_librarian.gpg
import nautilus_librarian.libvips
import typer
from typer.main import Typer

app: Typer = typer.Typer()


def add_subcommands():
    app.add_typer(nautilus_librarian.dvc.app, name="dvc")
    app.add_typer(nautilus_librarian.git.app, name="git")
    app.add_typer(nautilus_librarian.gpg.app, name="gpg")
    app.add_typer(nautilus_librarian.libvips.app, name="libvips")


@app.command()
def test(echo_string: str):
    typer.echo(f"Testing main module: {echo_string}")


if __name__ == "__main__":
    add_subcommands()
    app()
