from pathlib import Path
import re
import textwrap
from typing import List


def to_lex_uri(string: str, base_uri: str = None) -> str:
    if string.startswith("lex:"):
        return string

    if string.startswith("#"):
        if not base_uri:
            raise ValueError(f"Unable to resolve URI without anchor: {string}")
        return f"{base_uri}{string}"

    return f"lex:{string}"


# ==============================================================================

def ensure_path_and_init_files(path: Path):
    path_obj = Path(path)
    path_obj.mkdir(parents=True, exist_ok=True)
    init_file = path_obj / "__init__.py"
    init_file.touch()


def snake_to_camel(name: str) -> str:
    return "".join(x.capitalize() or "_" for x in name.split("_"))


def camel_to_snake(name: str) -> str:
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


def build_python_module_file_structure(output_dir: Path, id_str: str) -> Path:
    id_parts = id_str.split(".")
    package_names = id_parts[:-1]
    file_name = camel_to_snake(id_parts[-1]) + ".py"

    base_path = output_dir
    for package_name in package_names:
        base_path = base_path / package_name
        ensure_path_and_init_files(base_path)

    return base_path / file_name


def import_types_str(package_path: str, type_names: List[str], max_line=79) -> str:
    """
    Builds a string that imports the given type names from the given package path.
    Reformats the string to be within the given max_line length.
    """
    import_str = f'from {package_path} import {", ".join(type_names)}'
    if len(import_str) <= max_line:
        return import_str

    import_str = f"from {package_path} import (\n"
    import_str += "    " + textwrap.fill(
        ", ".join(type_names), max_line - 4, subsequent_indent="    "
    )
    import_str += "\n)"
    return import_str