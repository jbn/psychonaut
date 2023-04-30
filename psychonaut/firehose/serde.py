from typing import Any, Dict
import cbor2
import base64
import io
from pathlib import Path

from multiformats import CID
from pydantic import BaseModel

from psychonaut.firehose.car import read_car
import dag_cbor



def read_msg_pair(msg: bytes):
    with io.BytesIO(msg) as fp:
        kind = cbor2.load(fp)
        obj = dag_cbor.decode(fp.read())
    return kind, obj


def read_first_block(msg: bytes):
    kind, obj = read_msg_pair(msg)

    if "t" not in kind or kind["t"] != "#commit":
        return None

    # TODO: "t==#handle"

    blocks = read_car(obj["blocks"])

    obj["blocks"] = blocks

    return obj

    # return {
    #     'ks': list(obj.keys()),
    #     'repo': obj['repo'],
    #     'block': blocks
    # }



def _json_encode_kludge(d: Dict[Any, Any]) -> Any:
    for k, v in d.items():
        if isinstance(v, CID):
            d[k] = str(v)
        elif isinstance(v, bytes):
            d[k] = base64.b64encode(v).decode()
        elif isinstance(v, BaseModel):
            _json_encode_kludge(v.dict())
        elif isinstance(v, dict):
            _json_encode_kludge(v)
        elif isinstance(v, list):
            for i, x in enumerate(v):
                if isinstance(x, CID):
                    v[i] = str(x)
                elif isinstance(x, dict):
                    _json_encode_kludge(x)

    return d





