import click
from pathlib import Path
import json
from .util import print_error_and_fail
from .group import cli


@cli.command()
@click.argument("handle")
@click.option("--allow-overwrite", is_flag=True, default=False)
def save_login(handle: str, allow_overwrite: bool):
    file_path = Path().home() / ".psychonaut.json"

    if file_path.exists() and not allow_overwrite:
        print_error_and_fail(
            f"File {file_path} exists, use --allow-overwrite to overwrite"
        )

    # read the password
    password = click.prompt(f"Enter password for {handle}", hide_input=True)

    # write the file
    file_path.write_text(
        json.dumps(
            {
                "username": handle,
                "password": password,
            }
        )
    )
