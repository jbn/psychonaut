from typing import Any, Callable, Iterable

from pydantic import BaseModel
from carbox.car import read_car
from psychonaut.firehose.serde import read_event_pair, read_enriched_event


ERROR_CALLBACK_TYPE = Callable[[int, bytes], None]


def noop_error_callback(i: int, e: Exception, msg: bytes) -> None:
    pass


class ErrorCollector:
    def __init__(self):
        self.errors = []

    def __call__(self, i: int, e: Exception, msg: bytes) -> None:
        self.errors.append((i, e, msg))

    def __len__(self):
        return len(self.errors)


def iter_events(
    messages: Iterable[bytes], err_callback: ERROR_CALLBACK_TYPE = noop_error_callback
) -> Iterable[Any]:
    for i, msg in enumerate(messages):
        header, event = read_event_pair(msg)
        try:
            roots, blocks = read_car(event["blocks"])
            yield header, event, roots, blocks
        except KeyError as e:
            err_callback(i, e, msg)


def iter_enriched_events(
    messages: Iterable[bytes], err_callback: ERROR_CALLBACK_TYPE = noop_error_callback, with_messages=False
) -> Iterable[BaseModel]:
    for i, msg in enumerate(messages):
        try:
            if with_messages:
                yield read_enriched_event(msg), msg
            else:
                yield read_enriched_event(msg)
        except Exception as e:
            err_callback(i, e, msg)

