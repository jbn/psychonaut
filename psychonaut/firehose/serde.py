import json
from typing import Any, Dict
import cbor2
import base64
import io
from pathlib import Path
from psychonaut.firehose.car import parse_car_blocks


def read_msg_pair(msg: bytes):
    with io.BytesIO(msg) as fp:
        kind = cbor2.load(fp)
        obj = cbor2.load(fp)

    return kind, obj


def read_first_block(msg: bytes):
    kind, obj = read_msg_pair(msg)

    if kind["t"] != "#commit":
        return None
    
    # TODO: "t==#handle"

    first_block = parse_car_blocks(obj["blocks"])

    obj['first_block'] = first_block
    
    return {
        'ks': list(obj.keys()),
        'repo': obj['repo'],
        'blocks': first_block,
    }



def b64line_cbor2_iter(stream_path: Path):
    with stream_path.open() as f:
        for line in f:
            msg = base64.b64decode(line)

            yield read_msg_pair(msg)


def stream_to_stdout(b64line_file: Path):
    with open(b64line_file) as f:
        for line in f:
            msg = base64.b64decode(line)
            first_block = read_first_block(msg)

            if first_block:
                # TODO: finish pydantic models for records so no kludge needed
                line = json.dumps(_json_encode_kludge(first_block))
                print(line)


def _json_encode_kludge(d: Dict[Any, Any]) -> Any:
    # Recursively replace any value in the dict that is a CBORTag with a string
    for k, v in d.items():
        if isinstance(v, cbor2.CBORTag):
            d[k] = str(v)
        elif isinstance(v, bytes):
            d[k] = base64.b64encode(v).decode()
        elif isinstance(v, dict):
            _json_encode_kludge(v)
        elif isinstance(v, list):
            for i, x in enumerate(v):
                if isinstance(x, cbor2.CBORTag):
                    v[i] = str(x)
                elif isinstance(x, dict):
                    _json_encode_kludge(x)

    return d
