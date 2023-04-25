from pathlib import Path

from multiformats import CID
from psychonaut.firehose.car import parse_car_blocks
from psychonaut.firehose.serde import find_b64_line, read_msg_pair
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

    kind, obj = read_msg_pair(post)
    assert kind == {"op": 1, "t": "#commit"}

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
    assert set(obj) == keys

    assert len(obj["ops"]) == 1
    op = obj["ops"][0]
    assert op['action'] == 'create'
    assert op['path'] == 'app.bsky.feed.post/3ju35q7husm2p'
    cid = op['cid']
    assert isinstance(cid, CID)
    assert str(cid) == "zdpuAx7GYAybGShxy9wvkK5eJt6a5G47tz5z5yeFcDqChfYE3"
    
    assert obj['seq'] == 4715462
    assert isinstance(obj['prev'], CID)
    assert str(obj['prev']) == "zdpuAmv8cg3iFrz9rn14kYpCZDphscAnYxzxm8EKodWpXbRec"
    assert obj['repo'] == "did:plc:o32okshy54r5h2vlrjpz3aln"
    assert obj['time'] == "2023-04-23T23:05:15.389Z"

    assert len(obj['blobs']) == 0
    assert len(obj['blocks']) == 5082
    assert isinstance(obj['commit'], CID)
    assert str(obj['commit']) == "zdpuArKcqh4Bfc5ufSWKTSS1jFRYJ47gpuxCEVXeWdMEjDpAM"

    assert not obj['rebase']
    assert not obj['tooBig']


def test_parse_car_blocks(load_test_fixture):
    post = b64decode(load_test_fixture("donkeyballs.b64"))
    _, obj = read_msg_pair(post)
    blocks_raw = obj['blocks']
    blocks = parse_car_blocks(blocks_raw)

    assert len(blocks) == 10
    assert blocks[0] == {
        '$type': 'app.bsky.feed.post',
        'createdAt': '2023-04-23T23:05:15.184Z',
        'text': 'donkeyballs',
    }

    #assert blocks[2] == { }



