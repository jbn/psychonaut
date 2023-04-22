from psychonaut.cli.group import cli

# Imports to assemble the cli
from psychonaut.cli.config import * # noqa
from psychonaut.cli.stream import * # noqa
from psychonaut.cli.useful_queries import * # noqa
from psychonaut.cli.poasting import * # noqa
from psychonaut.cli.graph import * # noqa




# TODO: test poetry install
if __name__ == "__main__":
    cli()
