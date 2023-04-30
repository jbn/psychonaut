from __future__ import annotations
from collections import OrderedDict
from pathlib import Path
import textwrap
from typing import Union
import importlib
import black
from psychonaut.lexicon.constants import MODULE_PREFIX
from psychonaut.lexicon.ctx import GenCtx
from psychonaut.lexicon.fields import generate_pydantic_fields
from psychonaut.lexicon.planner import LexiconDef, compile_toposorted_lexicon_defns
from psychonaut.lexicon.types import (
    LexObject,
    LexRecord,
    LexRef,
    LexRefUnion,
    LexString,
    LexToken,
    LexXrpcParameters,
    LexXrpcProcedure,
    LexXrpcQuery,
)
from .util import (
    camel_to_class_name,
    camel_to_snake,
    import_types_str,
    build_python_module_file_structure,
)
from black import format_str, FileMode


def generate_all(
    input_dir: Path,
    output_dir: Path,
    verbose: bool = False,
    import_all_test: bool = False,
):
    # Create the output directory if it doesn't exist.
    # The ensure_path_and_init_files function will do this for us, but
    # it's nice to visibly mark progress.
    output_dir.mkdir(parents=True, exist_ok=True)

    # With the way we're generating and collecting code fragments,
    # we don't actually need to do a topological sort. But
    # doing so does some really helpful sanity checks early on.
    ctxs = OrderedDict()
    global_vars = {}
    global_vars['no_import'] = set()
    for node in compile_toposorted_lexicon_defns(input_dir):
        if verbose:
            # print(f"Processing {node.node_id} in {node.input_path}")
            pass

        # Generation contexts are at a per-file granularity.
        ctx = ctxs.get(node.input_path)
        if not ctx:
            ctx = GenCtx(
                verbose=verbose, input_path=node.input_path, global_vars=global_vars
            )
            ctx.imports["typing"].add("Any")  # TODO: ugly kludge
            ctxs[node.input_path] = ctx

        _generate_defn(ctx, node)

    # Write out all the generated code.
    # There are a few points during which things could still fail.
    # But having partial output is kinda convenient for debugging.
    module_paths = []
    for input_path, ctx in ctxs.items():
        module_paths.append(_write_generated(ctx, output_dir, verbose=verbose))

    if not import_all_test:
        return

    # It's a bit easier to try over all of them and then fail with the codegen.
    did_fail = False
    for module_path in module_paths:
        try:
            importlib.import_module(module_path)
        except Exception as e:
            print(f"!Failed to import {module_path}: {e}")
            did_fail = True
    
    if did_fail:
        raise Exception("Failed to import all generated modules")



# = Level 1 ==================================================================


def _generate_defn(ctx: GenCtx, node: LexiconDef):
    # The following is roughly in order of use frequency.
    # python (3.10) match statements aren't implemented with jump tables
    # so this prob has no effect on performance. But it does hint
    # at the order of importance for covering a lot of the lexicon.
    match node.defn.type:
        case "query":
            generate_query(ctx, node)
        case "procedure":
            generate_procedure(ctx, node)
        case "record":
            generate_record(ctx, node)
        case "object":
            generate_object(ctx, node)
        case "subscription":
            pass
        case "token":
            generate_token(ctx, node)
        case "string":
            generate_string(ctx, node)
        case _:
            raise Exception(f"Unknown defn type: {node.defn.type} in {node}")


def _write_generated(ctx: GenCtx, output_dir: Path, verbose: bool) -> str:
    code_blocks = [generate_imports(ctx)] + [
        frag.generated_src for frag in ctx.fragments.values()
    ]

    src = "\n".join(code_blocks)
    if not src.strip() or not ctx.common_xrpc_id:  # TODO: should never happen
        return

    output_path = build_python_module_file_structure(output_dir, ctx.common_xrpc_id)

    if verbose:
        print(f"\tWriting generated code to {output_path} {ctx.common_xrpc_id}")

    with open(output_path, "w") as f:
        # Black formatted. This is good because,
        # - it enforces a consistent style including in regenerated commits
        # - block does syntax validation so this is another sanity check
        black_formatted = ""
        try:
            black_formatted = format_str(src, mode=FileMode())
        except black.InvalidInput:
            print(f"Failed to format {output_path}")
            print(src)
            raise

        f.write(black_formatted)

    return MODULE_PREFIX + camel_to_snake(ctx.common_xrpc_id)


# = Level 2 ==================================================================


def _setup_and_validate(
    ctx: GenCtx,
    node: LexiconDef,
    expected_defn_type: type,
    log_message: str,
    skip_deps: bool = False,
):
    assert isinstance(
        node.defn, expected_defn_type
    ), f"{expected_defn_type.__name__} != {type(node.defn)}"

    if ctx.verbose:
        print(f"{log_message} {node.node_id}: {node.leaf_id_as_class_name}")

    if not skip_deps:
        _add_dep_imports(ctx, node)


def generate_query(ctx: GenCtx, node: LexiconDef):
    _setup_and_validate(ctx, node, LexXrpcQuery, "Generating query")

    # Queries use a Session object
    ctx.imports["psychonaut.api.session"].add("Session")

    blocks = []

    # If there is an output, generate the Resp first
    resp_name = "Any"
    if output := node.defn.output:
        if isinstance(output.schema_kludge, LexObject):
            resp_name = node.leaf_id_as_class_name + "Resp"
            desc = output.description or output.schema_kludge.description
            blocks.append(
                generate_pydantic_model(
                    ctx,
                    resp_name,
                    desc,
                    output.schema_kludge or {},
                )
            )
        elif isinstance(output.schema_kludge, LexRef):
            print("REF", output)
        elif isinstance(output.schema_kludge, LexRefUnion):
            print("REF UNION", output)
        else:
            print("UNKNOWN", output)

    # There must always be a request class for Psychonaut
    req_name = node.leaf_id_as_class_name + "Req"
    blocks.append(
        generate_pydantic_model(
            ctx,
            req_name,
            node.defn.description or "[none provided by spec]",
            node.defn.parameters or {},
        )
    )
    blocks.append(_generate_xrpc_id_property(node))

    blocks.append(
        build_async_session_f(
            ctx,
            "query",
            resp_name,
        )
    )

    node.generated_src = "\n\n".join(blocks)

    ctx.add_fragment(req_name, node)


def generate_procedure(ctx: GenCtx, node: LexiconDef):
    _setup_and_validate(ctx, node, LexXrpcProcedure, "Generating procedure")

    # Procedures use a Session object
    ctx.imports["psychonaut.api.session"].add("Session")

    # Procedures area little trickier than quries because
    # they may have both parameters and an input.
    assert not (
        node.defn.input and node.defn.parameters
    ), f"procedure {node.node_id} input and parameters"
    req_schema = {}
    if node.defn.input:
        req_schema = node.defn.input.schema_kludge
    elif node.defn.parameters:
        req_schema = node.defn.parameters.schema_json

    blocks = []

    # If there is an output, generate the Resp first
    resp_name = "Any"
    if output := node.defn.output:
        if isinstance(output.schema_kludge, LexObject):
            resp_name = node.leaf_id_as_class_name + "Resp"
            desc = output.description or output.schema_kludge.description
            blocks.append(
                generate_pydantic_model(
                    ctx,
                    resp_name,
                    desc,
                    output.schema_kludge or {},
                )
            )
        elif isinstance(output.schema_kludge, LexRef):
            print("REF", output)
        elif isinstance(output.schema_kludge, LexRefUnion):
            print("REF UNION", output)
        else:
            print("UNKNOWN", output)

    # There must always be a request class for Psychonaut
    req_name = node.leaf_id_as_class_name + "Req"

    blocks.append(
        generate_pydantic_model(
            ctx,
            req_name,
            node.defn.description or "[none provided by spec]",
            req_schema,
        )
    )
    blocks.append(_generate_xrpc_id_property(node))
    blocks.append(
        build_async_session_f(
            ctx,
            "procedure",
            resp_name,
        )
    )

    node.generated_src = "\n\n".join(blocks)
    ctx.add_fragment(req_name, node)


def generate_record(ctx: GenCtx, node: LexiconDef):
    _setup_and_validate(ctx, node, LexRecord, "Generating record")

    blocks = []
    class_name = node.leaf_id_as_class_name
    blocks.append(
        generate_pydantic_model(
            ctx,
            node.leaf_id_as_class_name,
            node.defn.description or "[none provided by spec]",
            node.defn.record or {},
        )
    )
    blocks.append(_generate_xrpc_id_property(node))

    node.generated_src = "\n\n".join(blocks)
    ctx.add_fragment(class_name, node)


def generate_object(ctx: GenCtx, node: LexiconDef):
    _setup_and_validate(ctx, node, LexObject, "Generating object")

    # app.bsky.embed.externa.json is annoying because the main is an object and so is the external
    # TODO: figure out how to handle this
    obj_name = node.leaf_id_as_class_name
    if node.node_id == "app.bsky.embed.external" and len(node.defn.properties) == 1:
        obj_name = "ExternalFML"

    blocks = []
    blocks.append(
        generate_pydantic_model(
            ctx,
            node.leaf_id_as_class_name,
            node.defn.description or "[none provided by spec]",
            node.defn or {},
        )
    )

    node.generated_src = "\n\n".join(blocks)
    ctx.add_fragment(obj_name, node)


def generate_string(ctx: GenCtx, node: LexiconDef):
    _setup_and_validate(ctx, node, LexString, "Generating object", skip_deps=True)
    ctx.imports["enum"].update(["Enum", "auto"])

    lines = [f"class {node.leaf_id_as_class_name}(str, Enum):"]
    for dep in node.deps:
        # TODO: add description
        tok = ctx.global_vars[dep]
        as_constant = camel_to_class_name(tok.leaf_id).upper()
        lines.append(f"    {as_constant} = {repr(tok.leaf_id)}")

    node.generated_src = "\n".join(lines)
    ctx.add_fragment(node.leaf_id_as_class_name, node)


def generate_token(ctx: GenCtx, node: LexiconDef):
    assert isinstance(node.defn, LexToken), f"LexToken != {type(node.defn)}"
    if ctx.verbose:
        print(f"Generating token {node.node_id}: {node.leaf_id_as_class_name}")

    ctx.global_vars[node.node_id] = node
    ctx.global_vars['no_import'].add(node.node_id)


# = Level 3 ==================================================================


def _generate_xrpc_id_property(node: LexiconDef) -> str:
    return f"""
    @property
    def xrpc_id(self) -> str:
        return "{node.node_id}"
    """


def generate_pydantic_model(
    ctx: GenCtx,
    class_name: str,
    docstr: str,
    params: Union[LexXrpcParameters, LexObject],
    parent_class: str = "BaseModel",
) -> str:
    """
    Generate a pydantic model class from the given parameters.

    :param ctx: The generation context (save things like imports)
    :param class_name: The name of the class to generate
    :param docstr: The docstring for the class
    :param params: The parameters to generate the class from
    """
    model_lines = []

    # Signal that we need to import pydantic's basemodel
    ctx.imports["pydantic"].add(parent_class)

    # Generate the pydantic fields (if any)
    field_lines = generate_pydantic_fields(ctx, params)
    if field_lines:
        ctx.imports["pydantic"].add("Field")

    model_lines.append(f"class {class_name}(BaseModel):")
    if docstr:
        model_lines.append(generate_class_docstr(docstr))

    for field_line in field_lines:
        model_lines.append(f"    {field_line}")

    model_lines.append("")

    return "\n".join(model_lines)


def generate_class_docstr(docstr: str) -> str:
    return "\n".join(
        [
            '    """',
            textwrap.fill(
                docstr, width=76, initial_indent="    ", subsequent_indent="    "
            ),
            '    """',
        ]
    )


def generate_imports(ctx: GenCtx) -> str:
    model_lines = []
    names_seen, shadow_detected = set(), False
    for import_path, type_names in ctx.imports.items():
        model_lines.append(import_types_str(import_path, type_names))
        for name in type_names:
            if name in names_seen:
                shadow_detected = True
            names_seen.add(name)

    if shadow_detected:
        print(f"WARNING: shadowing imports detected in {ctx.common_xrpc_id}")
    model_lines.append("\n")

    return "\n".join(model_lines)


def build_async_session_f(ctx: GenCtx, f: "query", resp_class: str) -> str:
    ctx.imports["psychonaut.api.session"].add("Session")
    model_lines = []
    model_lines.append(f"    async def do_xrpc(self, sess: Session) -> {resp_class}:")

    if resp_class == "Any":
        model_lines.append(f"        return await sess.{f}(self)")
    else:
        model_lines.append(f"        resp = await sess.{f}(self)")
        model_lines.append(f"        return {resp_class}(**resp)")
    return "\n".join(model_lines)


def _add_dep_imports(ctx: GenCtx, node: LexiconDef):
    for dep in node.deps:
        if "#" not in dep:
            continue
        module, obj = dep.split("#")

        if module == ctx.common_xrpc_id:
            continue

        if dep in ctx.global_vars['no_import']:
            continue

        module = camel_to_snake(module)
        ctx.imports[MODULE_PREFIX + module].add(camel_to_class_name(obj))
