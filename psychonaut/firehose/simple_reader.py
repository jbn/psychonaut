from typing import Any, Iterable
from psychonaut.firehose.car import read_car

from psychonaut.firehose.serde import read_msg_pair


def iter_events(messages: Iterable[bytes], err_callback) -> Iterable[Any]:
    for i, msg in enumerate(messages):
        kind, obj = read_msg_pair(msg)
        try:
            roots, blocks = read_car(obj['blocks'])
            yield kind, obj, roots, blocks
        except KeyError:
            err_callback(i, msg)

