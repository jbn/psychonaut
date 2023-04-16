import json
from pathlib import Path
from typing import Iterable
import jmespath


def collect_all_values(lexicon_dir: str, query: str, transform=lambda d: d) -> Iterable[str]:
    """
    Iterate over every .json file in the lexicon directory and collect all values
    """
    for lexicon_file in Path(lexicon_dir).glob("**/*.json"):
        with open(lexicon_file, "r") as f:
            lexicon = json.load(f)
            res = jmespath.search(query, lexicon)
            if res:
                res = transform(res)
                for value in res:
                    yield value



def find_doc_match(lexicon_dir: str, pred_f=lambda d: bool):
    for lexicon_file in Path(lexicon_dir).glob("**/*.json"):
        with open(lexicon_file, "r") as f:
            src = f.read()
            lexicon = json.loads(src)

            if pred_f(lexicon):
                print(lexicon_file)
                print(src)
                print()