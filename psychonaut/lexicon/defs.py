

import json
from pathlib import Path
from psychonaut.lexicon.types import LexiconDoc


def generate_defs_from(file_path: Path, output_dir: Path, verbose: bool = False):
    # Load the LexiconDoc
    with open(file_path, "r") as json_file:
        doc = LexiconDoc(**json.load(json_file))

    defs = doc.defs
    if not defs:
        return

    print(doc.id)
    
    for k, defn in doc.defs.items():
        if defn.type != "object":
            continue

        props = defn.properties
        if not props:
            continue

        for k, v in props.items():
            if v.type == "ref":
                ref = v.ref
                if ref.startswith("#"):
                    ref = f"{doc.id}{ref}"
                print(f"\tFound ref: {k} -> {ref}")

