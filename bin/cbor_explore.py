from pprint import pprint
import json
from pathlib import Path
from typing import Any, Dict
import cbor2
import io
import base64
from multiformats import CID


def jsonl_cbor2_iter(path: Path):
    with stream_path.open() as f:
        for line in f:
            msg = base64.b64decode(line)

            with io.BytesIO(msg) as fp:
                kind = cbor2.load(fp)
                obj = cbor2.load(fp)

            yield kind, obj



def recursively_find_cbortag_objs(d: Dict[Any, Any], indent="    "):
    for k, v in d.items():
        if isinstance(v, cbor2.CBORTag):
            print(f"{indent}{k}: {v}")


# Op in commit is cid, path, action


class EventHeader:
    op: int
    t: str


STREAM_DIR = Path(__file__).parent.parent / "streams"
print(STREAM_DIR)

MSG_TYPES = {'#handle', '#commit'}
known_t = set()
for stream_path in STREAM_DIR.glob("*.jsonl"):
    print(stream_path)
    # op=1, t=#handle
    for kind, obj in jsonl_cbor2_iter(stream_path):
        pprint(kind)

        if kind['t'] == '#handle':
            #pprint.pprint(obj)
            pass
        elif kind['t'] == '#commit':
            print(obj['repo'])
            for op in obj['ops']:
                print(op)
                # print("\t", op)
                # cid_cbor = op['cid']
                # print(type(cid_cbor))
                # print(cid_cbor)

                # v = cid_cbor.value
                # x = CID.decode(v)
                # print(x)
            pprint(obj, indent=4)
            break
                #cid_cbor = CID.decode(cid_cbor.value)
                #recursively_find_cbortag_objs(op, indent="\t\t")

                # if op['path'].startswith("app.bsky.graph.follow"):
                #     print("\t\t", op)
                #     print("\t\t", op['cid'])

        else:
            if kind['t'] not in known_t:
                print(kind)

        # repo = obj['repo']
        # time = obj['time']
        # too_big = obj['tooBig']
        # ops = obj['ops']

        # print(kind, repo)
        # pprint.pprint(ops, indent=4)