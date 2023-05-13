from pathlib import Path

from multiformats import CID
from carbox.message import read_event_pair
from psychonaut.util import load_test_fixture
from base64 import b64decode


# def test_find_b64_line():
#     file_path = Path("/home/generativist/Social/bluesky/psychonaut/streams/stream.1682291107.b64-lines")

#     def predicate(kind, obj):
#         if 'block' not in obj:
#             return False

#         block = obj['block']
#         if not block:
#             return False

#         if 'text' not in block:
#             return False


#         return 'donkeyballs' in block['text']

#     line = find_b64_line(file_path, predicate)
#     print(line)

#     assert line == "d"


def test_read_msg_pair(load_test_fixture):
    post = b64decode(load_test_fixture("donkeyballs.b64"))

    header, event = read_event_pair(post)
    assert header == {"op": 1, "t": "#commit"}

    keys = {
        "ops",
        "seq",
        "prev",
        "repo",
        "time",
        "blobs",
        "blocks",
        "commit",
        "rebase",
        "tooBig",
    }
    assert set(event) == keys

    assert len(event["ops"]) == 1
    op = event["ops"][0]
    assert op["action"] == "create"
    assert op["path"] == "app.bsky.feed.post/3ju35q7husm2p"
    cid = op["cid"]
    assert isinstance(cid, CID)
    assert str(cid) == "zdpuAx7GYAybGShxy9wvkK5eJt6a5G47tz5z5yeFcDqChfYE3"

    assert event["seq"] == 4715462
    assert isinstance(event["prev"], CID)
    assert str(event["prev"]) == "zdpuAmv8cg3iFrz9rn14kYpCZDphscAnYxzxm8EKodWpXbRec"
    assert event["repo"] == "did:plc:o32okshy54r5h2vlrjpz3aln"
    assert event["time"] == "2023-04-23T23:05:15.389Z"

    assert len(event["blobs"]) == 0
    assert len(event["blocks"]) == 5082
    assert isinstance(event["commit"], CID)
    assert str(event["commit"]) == "zdpuArKcqh4Bfc5ufSWKTSS1jFRYJ47gpuxCEVXeWdMEjDpAM"

    assert not event["rebase"]
    assert not event["tooBig"]

    # assert blocks[2] == { }
