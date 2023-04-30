import shutil
import click
from pathlib import Path
from psychonaut.lexicon.codegen import generate_all


@click.command()
# Add the input directory (which must exist!)
@click.option(
    "--input-dir",
    default="lexicons",
    help="The input directory for the lexicon json files.",
    type=click.Path(exists=True),
)
@click.option(
    "--output-dir",
    default="psychonaut/api/lexicons",
    type=click.Path(exists=False),
    help="The output directory for the generated lexicon files.",
)
@click.option(
    "--remove-existing",
    default=False,
    type=bool,
    help="Whether to remove existing files in the output directory.",
    is_flag=True,
)
@click.option(
    "--verbose",
    default=False,
    type=bool,
    help="Whether to print verbose output.",
    is_flag=True,
)
@click.option(
    "--import-all-test",
    default=False,
    type=bool,
    help="Test the generated code by importing all the generated files.",
    is_flag=True,
)
def main(input_dir: str, output_dir: str, remove_existing: bool, verbose: bool, import_all_test: bool):
    if remove_existing and Path(output_dir).exists():
        if verbose:
            print(f"Removing existing files in {output_dir}")

        shutil.rmtree(output_dir)

    generate_all(
        input_dir=Path(input_dir),
        output_dir=Path(output_dir),
        verbose=verbose,
        import_all_test=import_all_test,
    )


if __name__ == "__main__":
    main()
