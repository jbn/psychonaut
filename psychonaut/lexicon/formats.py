import re
from multiformats import CID
from psychonaut.nsid.nsid import ensure_valid_nsid, InvalidNsidError
from psychonaut.identifier.did import ensure_valid_did
from psychonaut.identifier.handle import ensure_valid_handle
from psychonaut.uri.validation import ensure_valid_at_uri
from typing import Callable

# https://github.com/bluesky-social/atproto/blob/main/packages/lexicon/src/validators/formats.ts

URI_RE = re.compile(r"^\w+:(?:\/\/)?[^\s/][^\s]*$")
ISO8601_RE = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,3})?(Z|[+-]\d{2}:\d{2})$"
)


def validate_datetime(s: str):
    """
    Returns True if the string is a valid RFC 3339 datetime.
    """
    try:
        if ISO8601_RE.match(s) is not None:
            return
    except ValueError:
        pass
    raise ValueError(f"Invalid datetime: {s}")


def validate_uri(s: str):
    try:
        if URI_RE.match(s) is not None:
            return
    except ValueError:
        pass
    raise ValueError(f"Invalid URI: {s}")


def validate_at_uri(s: str):
    try:
        ensure_valid_at_uri(s)
        return
    except ValueError as e:
        raise ValueError(f"Invalid AT URI: {s}: {e}")


def validate_array(f: Callable[[str], None]):
    return lambda s: [f(x) for x in s]


def validate_nsid(s: str):
    try:
        ensure_valid_nsid(s)
        return
    except (InvalidNsidError, ValueError) as e:
        raise ValueError(f"Invalid NSID: {s}: {e}")


def validate_cid(s: str):
    try:
        CID.decode(s)
        return
    except ValueError as e:
        raise ValueError(f"Invalid CID: {s}: {e}")
    except KeyError as e:
        raise ValueError(f"Invalid CID: {s}: {e}")


def validate_did(s: str):
    ensure_valid_did(s)


def validate_handle(s: str):
    ensure_valid_handle(s)


def validate_at_identifier(s: str):
    try:
        validate_did(s)
    except ValueError:
        validate_handle(s)