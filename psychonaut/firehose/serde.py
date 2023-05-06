from typing import Any, Dict
import cbor2
import base64
import io
from multiformats import CID
from pydantic import BaseModel

from psychonaut.core.car import read_car
import dag_cbor

from psychonaut.firehose.events import CommitEvt, HandleEvt


def read_event_pair(msg: bytes):
    with io.BytesIO(msg) as fp:
        header = cbor2.load(fp)
        event = dag_cbor.decode(fp.read())
    return header, event


class UnknownKludge(BaseModel):
    header: Dict[str, Any]
    event: Dict[str, Any]


def read_enriched_event(msg: bytes):
    header, event = read_event_pair(msg)

    match header["t"]:
        case "#commit":
            return CommitEvt.parse_obj(event)
        case "#handle":
            return HandleEvt.parse_obj(event)
        case _:
            return UnknownKludge(header=header, event=event)


def read_first_block(msg: bytes):
    header, event = read_event_pair(msg)

    if "t" not in header or header["t"] != "#commit":
        return None

    # TODO: "t==#handle"

    blocks = read_car(event["blocks"])

    event["blocks"] = blocks

    return event

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
