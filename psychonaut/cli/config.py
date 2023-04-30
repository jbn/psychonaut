import click
from psychonaut.client.credentials import write_homedir_creds
from .util import print_error_and_fail
from .group import cli


@cli.command()
@click.argument("handle")
@click.option("--allow-overwrite", is_flag=True, default=False)
def save_login(handle: str, allow_overwrite: bool):
    try:
        with write_homedir_creds(handle, allow_overwrite) as f:
            f(click.prompt(f"Enter password for {handle}", hide_input=True))
    except FileExistsError as e:
        print_error_and_fail(f"{e}: use --allow-overwrite to overwrite")
