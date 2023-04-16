from __future__ import annotations
import json
from pathlib import Path
import textwrap
from typing import Union
from psychonaut.lexicon.ctx import GenCtx
from psychonaut.lexicon.fields import generate_pydantic_fields
from psychonaut.lexicon.types import (
    LexObject,
    LexXrpcBody,
    LexXrpcParameters,
    LexXrpcQuery,
    LexiconDoc,
)
from .util import (
    camel_to_snake,
    import_types_str,
    snake_to_camel,
    build_python_module_file_structure,
)


def generate_all(input_dir: Path, output_dir: Path, verbose: bool = False):
    # Create the output directory if it doesn't exist.
    # The ensure_path_and_init_files function will do this for us, but
    # it's nice to visibly mark progress.
    output_dir.mkdir(parents=True, exist_ok=True)

    results = {}

    for file_path in input_dir.glob("**/*.json"):
        if verbose:
            # print(f"Processing {file_path}")
            pass

        if file_path.name == "defs.json":
            # generate_defs_from(file_path, output_dir)
            generate(file_path, output_dir)
        else:
            res = generate(file_path, output_dir)


def generate(file_path: Path, output_dir: Path):
    # Load the LexiconDoc
    with open(file_path, "r") as json_file:
        doc = LexiconDoc(**json.load(json_file))

    defs = doc.defs
    # if not (
    #     defs and "main" in defs and len(defs) == 1 and defs["main"].type == "query"
    # ):
    #     return

    if not defs:
        return

    output_path = build_python_module_file_structure(output_dir, doc.id)

    if is_query(doc):
        model_base_name = snake_to_camel(output_path.stem)
        src = build_simple_query(model_base_name, doc)
    elif is_record(doc):
        print("!!!", file_path)
        model_base_name = snake_to_camel(output_path.stem)
        src = build_record(model_base_name, doc)
    else:
        src = ""

    with output_path.open("w") as fp:
        fp.write(src)


def is_query(doc: LexiconDoc) -> bool:
    defs = doc.defs

    if not defs:
        return False

    if "main" not in defs or defs["main"].type != "query":
        return False

    return True


def is_record(doc: LexiconDoc) -> bool:
    defs = doc.defs

    if not defs:
        return False

    if "main" not in defs or defs["main"].type != "record":
        return False

    return True


def build_simple_query(model_base_name: str, doc: LexiconDoc) -> str:
    ctx = GenCtx()

    main = doc.defs["main"]
    req_class_name = f"{model_base_name}Req"
    # if main.output:
    #     print(type(main))
    #     print(model_base_name)

    req_class = build_req_class(ctx, doc.id, model_base_name, main)

    resp_class = None
    if main.output:
        resp_class = build_resp_class(ctx, doc.id, model_base_name, main.output)

    ctx.imports["psychonaut.api.session"].add("Session")
    ctx.imports["typing"].add("Any")
    ctx.imports["typing"].add("Optional")

    model_lines = []
    model_lines.append(build_imports(ctx))
    model_lines.append(req_class)
    if resp_class:
        model_lines.append(resp_class)

    model_lines.append(
        build_async_session_f(
            ctx,
            model_base_name,
            "query",
            req_class_name,
            f"{model_base_name}Resp" if resp_class else "Any",
        )
    )

    model_lines.append("")
    src = "\n".join(model_lines)

    return src


def build_record(model_base_name: str, doc: LexiconDoc) -> str:
    ctx = GenCtx()

    main = doc.defs["main"]
    req_class_name = f"{model_base_name}Req"
    # if main.output:
    #     print(type(main))
    #     print(model_base_name)

    req_class = build_req_class(ctx, doc.id, model_base_name, main.record)

    # resp_class = None
    # if main.output:
    #     resp_class = build_resp_class(ctx, doc.id, model_base_name, main.output)

    ctx.imports["psychonaut.api.session"].add("Session")
    ctx.imports["typing"].add("Any")
    ctx.imports["typing"].add("Optional")

    model_lines = []
    model_lines.append(build_imports(ctx))
    model_lines.append(req_class)

    resp_class = ""

    model_lines.append(
        build_async_session_f(
            ctx,
            model_base_name,
            "record",
            req_class_name,
            f"{model_base_name}Resp" if resp_class else "Any",
        )
    )
    # if resp_class:
    #     model_lines.append(resp_class)
    # model_lines.append(
    #     build_async_query(
    #         ctx,
    #         model_base_name,
    #         req_class_name,
    #         f"{model_base_name}Resp" if resp_class else "Any",
    #     )
    # )

    model_lines.append("")
    src = "\n".join(model_lines)

    return src


def build_imports(ctx: GenCtx) -> str:
    model_lines = []
    for import_path, type_names in ctx.imports.items():
        model_lines.append(import_types_str(import_path, type_names))
    model_lines.append("\n")

    return "\n".join(model_lines)


def build_async_session_f(
    ctx: GenCtx, model_base_name: str, f: "query", req_class: str, resp_class: str
) -> str:
    ctx.imports["psychonaut.api.session"].add("Session")

    func_name = camel_to_snake(model_base_name)
    model_lines = []
    model_lines.append(
        f"async def {func_name}(sess: Session, req: {req_class}) -> {resp_class}:"
    )

    if resp_class == "Any":
        model_lines.append(f"    return await sess.{f}(req)")
    else:
        model_lines.append(f"    resp = await sess.{f}(req)")
        model_lines.append(f"    return {resp_class}(**resp)")
    return "\n".join(model_lines)


def build_req_class(
    ctx: GenCtx, xrpc_id: str, model_base_name: str, main: LexXrpcQuery
) -> str:
    docstr = main.description or ""
    class_name = f"{model_base_name}Req"

    params = None
    if hasattr(main, "parameters"):
        params = main.parameters
    else:
        params = {}
        # print(main)
        params = main

    model_lines = [generate_pydantic_model(ctx, class_name, docstr, params)]
    model_lines.append("    @property")
    model_lines.append("    def xrpc_id(self) -> str:")
    model_lines.append(f'       return "{xrpc_id}"')
    model_lines.append("\n")

    src = "\n".join(model_lines)

    return src


def build_resp_class(
    ctx: GenCtx, xrpc_id: str, model_base_name: str, output: LexXrpcBody
) -> str:
    docstr = output.description or ""
    class_name = f"{model_base_name}Resp"

    if not isinstance(output.schema_kludge, LexObject):
        print("Not an object:", model_base_name)
        return ""

    props = output.schema_kludge.properties
    if not props:
        print("No properties:", model_base_name)
        return ""

    model_lines = [
        generate_pydantic_model(ctx, class_name, docstr, output.schema_kludge)
    ]
    model_lines.append("    @property")
    model_lines.append("    def xrpc_id(self) -> str:")
    model_lines.append(f'       return "{xrpc_id}"')
    model_lines.append("\n")

    src = "\n".join(model_lines)

    return src


def generate_pydantic_model(
    ctx: GenCtx,
    class_name: str,
    docstr: str,
    params: Union[LexXrpcParameters, LexObject],
) -> str:
    model_lines = []

    # Signal that we need to import pydantic's basemodel
    ctx.imports["pydantic"].add("BaseModel")

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
