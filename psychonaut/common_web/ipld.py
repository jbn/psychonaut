"""
https://github.com/bluesky-social/atproto/blob/d8b50c73e4915277da049e18cd5f6296d978aff4/packages/common-web/src/ipld.ts
"""
from multiformats.cid import CID
from typing import Any, Dict, List, Optional, Union
import base64

# TODO: untested mostly

JsonValue = Union[bool, float, str, None, Any, List[Any], Dict[str, Any]]
IpldValue = Union[JsonValue, CID, bytes, List[Any], Dict[str, Any]]


def as_cid(obj) -> Optional[CID]:
    if isinstance(obj, CID):
        return obj

    if isinstance(obj, (str, bytes)):
        try:
            return CID.decode(obj)
        except (ValueError, KeyError):
            return None

    return None


def json_to_ipld(val: JsonValue) -> IpldValue:
    if isinstance(val, list):
        return [json_to_ipld(item) for item in val]

    if val and isinstance(val, dict):
        if "$link" in val and len(val) == 1:
            return CID.decode(val["$link"])

        if "$bytes" in val and len(val) == 1:
            return base64.b64decode(val["$bytes"])

        return {key: json_to_ipld(val[key]) for key in val.keys()}

    return val


def ipld_to_json(val: IpldValue) -> JsonValue:
    if isinstance(val, list):
        return [ipld_to_json(item) for item in val]

    if val:
        if isinstance(val, bytes):
            return {"$bytes": base64.b64encode(val).decode("utf-8")}

        if (cid := as_cid(val)) is not None:
            return {"$link": str(cid)}

        if isinstance(val, dict):
            return {key: ipld_to_json(val[key]) for key in val.keys()}

    return val


def ipld_equals(a: IpldValue, b: IpldValue) -> bool:
    if isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            return False

        for i in range(len(a)):
            if not ipld_equals(a[i], b[i]):
                return False

        return True

    if a and b:
        if isinstance(a, bytes) and isinstance(b, bytes):
            return a == b

        if (a_cid := as_cid(a)) and (b_cid := as_cid(b)):
            # TODO: what is correct equality
            return a_cid == b_cid

        if isinstance(a, dict) and isinstance(b, dict):
            if len(a.keys()) != len(b.keys()):
                return False

            for key in a.keys():
                if not ipld_equals(a[key], b[key]):
                    return False
            return True

    return a == b
