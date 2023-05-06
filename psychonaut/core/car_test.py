from multiformats import CID
from base64 import b64decode
from psychonaut.core.car import read_car
from psychonaut.firehose.serde import read_event_pair
from psychonaut.util import load_test_fixture


def test_read_car(load_test_fixture):
    post = b64decode(load_test_fixture("donkeyballs.b64"))
    _, event = read_event_pair(post)
    blocks_raw = event["blocks"]
    roots, blocks = read_car(blocks_raw)

    assert [str(cid) for cid in roots] == [
        "zdpuArKcqh4Bfc5ufSWKTSS1jFRYJ47gpuxCEVXeWdMEjDpAM"
    ]
    assert len(blocks) == 10

    assert blocks[0].cid == CID.decode(
        "zdpuAx7GYAybGShxy9wvkK5eJt6a5G47tz5z5yeFcDqChfYE3"
    )
    assert blocks[0].decoded == {
        "$type": "app.bsky.feed.post",
        "createdAt": "2023-04-23T23:05:15.184Z",
        "text": "donkeyballs",
    }
