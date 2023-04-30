from graphlib import TopologicalSorter
from pathlib import Path
from typing import Dict, List, Optional, Set, Union
from pydantic import BaseModel, Field
from psychonaut.lexicon.types import (
    LexArray,
    LexRef,
    LexRefUnion,
    LexString,
    LexiconDoc,
)
from psychonaut.lexicon.util import (
    camel_to_snake,
    memoized_property,
    camel_to_class_name,
)


class LexiconDef(BaseModel):
    node_id: str
    deps: Set[str] = Field(default_factory=set)
    input_path: Path
    defn: BaseModel = Field(repr=False)

    generated_src: Optional[str] = Field(default=None, repr=False)

    @memoized_property
    def leaf_id(self) -> str:
        parts = self.node_id.split("#")
        if len(parts) == 2:
            return parts[1]

        parts = self.node_id.split(".")
        if len(parts) > 1:
            return parts[-1]

        raise ValueError(f"Unable to determine leaf id for {self.node_id}")

    @memoized_property
    def leaf_id_snake(self) -> str:
        return camel_to_snake(self.leaf_id)

    @memoized_property
    def leaf_id_as_class_name(self) -> str:
        return camel_to_class_name(self.leaf_id)


def create_plan(input_dir: Path):
    for node in compile_toposorted_lexicon_defns(input_dir):
        print(node.node_id, node.defn.type)


def compile_toposorted_lexicon_defns(input_dir: Path) -> List[LexiconDef]:
    def_id_to_lexicon_def = {}
    graph: Dict[str, Set[str]] = {}

    # Collect all the defs in the first pass.
    for input_path in input_dir.glob("**/*.json"):
        # Parse the document once.
        doc = LexiconDoc.parse_file(input_path)

        parent_xrpc_id = doc.id

        # Anything at this level has a defs section.
        for k, defn in doc.defs.items():
            # maybe NSID? but with fragment?
            def_id = f"{doc.id}#{k}" if k != "main" else doc.id

            graph[def_id] = _extract_deps_from_base_model(parent_xrpc_id, def_id, defn)

            def_id_to_lexicon_def[def_id] = LexiconDef(
                node_id=def_id,
                deps=graph[def_id].copy(),
                input_path=input_path,
                defn=defn,
            )

    # Do topo sort to check for cycles first.
    nodes = list(TopologicalSorter(graph).static_order())

    # Identify missing. If there are any, we can't continue.
    missing = set(n for n in nodes if n not in def_id_to_lexicon_def)
    if missing:
        print("MISSING DEFINITIONS FOR:")
        for k in missing:
            print(f"\t{k}")
        return []

    return [def_id_to_lexicon_def[k] for k in nodes]


def _extract_deps_from_base_model(
    parent_xrpc_id: str, def_id: str, defn: BaseModel
) -> Set[str]:
    deps = set()

    for field in defn.__fields__:
        _extract_deps(parent_xrpc_id, getattr(defn, field, None), deps)

    if def_id in deps:
        deps.remove(def_id)  # cycle

    if def_id == "app.bsky.embed.record#viewRecord":
        print("MANGLING app.bsky.embed.record#viewRecord cycle")
        return set()  # TODO: cycle break kludge

    return deps


def _extract_deps(
    parent_xrpc_id: str, defn, deps: Optional[Set[str]] = None
) -> Set[str]:
    if deps is None:
        deps = set()

    if defn is None:
        return deps

    if isinstance(defn, list) and len(defn) > 0 and isinstance(defn[0], str):
        # Kludge for knownValues
        for item in defn:
            if "#" in item:
                deps.add(_fully_qualified_ref(parent_xrpc_id, item))

    if not isinstance(defn, dict):
        # TODO: ugly as fuck
        if isinstance(defn, BaseModel):
            for field in defn.__fields__:
                _extract_deps(parent_xrpc_id, getattr(defn, field, None), deps)
            return
        else:
            return deps

    for k, v in defn.items():
        # If the value is a dict, recurse
        if isinstance(v, dict):
            _extract_deps(parent_xrpc_id, v, deps)
        # If the value is a list, recurse
        elif isinstance(v, list):
            for item in v:
                _extract_deps(parent_xrpc_id, item, deps)
        elif isinstance(v, (LexRef, LexRefUnion)):
            _extract_ref_deps_from(deps, parent_xrpc_id, v)
        elif isinstance(v, LexArray):
            _extract_ref_deps_from(deps, parent_xrpc_id, v.items)
        elif isinstance(v, LexString):
            _extract_ref_deps_from_lex_string(deps, parent_xrpc_id, v)
        elif isinstance(v, str):
            raise "A"
            if v.startswith("#"):
                deps.add(_fully_qualified_ref(parent_xrpc_id, v))

    return deps


def _extract_ref_deps_from(
    deps: Set[str], parent_xrpc_id, v: Union[LexRefUnion, LexRef]
) -> Set[str]:
    if isinstance(v, LexRef):
        deps.add(_fully_qualified_ref(parent_xrpc_id, v.ref))
    elif isinstance(v, LexRefUnion):
        deps.update(_fully_qualified_ref(parent_xrpc_id, ref) for ref in v.refs)


def _extract_ref_deps_from_lex_string(
    deps: Set[str], parent_xrpc_id: str, v: LexString
):
    if v.known_values:
        known_values = {
            _fully_qualified_ref(parent_xrpc_id, item)
            for item in v.known_values
            if "#" in item
        }
        if known_values:
            deps.update(known_values)


def _fully_qualified_ref(parent_xrpc_id: str, ref: str) -> str:
    if ref.startswith("#"):
        ref = f"{parent_xrpc_id}{ref}"
    return ref
