"""
More or less a GPT-4 translation of the NSID code from:
https://github.com/bluesky-social/atproto/blob/656be937a52688601c088f5aa332137dfaf019cf/packages/nsid/src/index.ts
"""
import re
from pydantic import BaseModel, validator
from typing import List

class NSID(BaseModel):
    """
    Namespaced IDs
    """
    segments: List[str]

    @classmethod
    def parse(cls, nsid: str):
        ensure_valid_nsid(nsid)
        segments = nsid.split('.')
        return cls(segments=segments)

    @classmethod
    def create(cls, authority: str, name: str):
        segments = authority.split('.')[::-1] + [name]
        nsid = '.'.join(segments)
        return cls.parse(nsid)

    @classmethod
    def is_valid(cls, nsid: str) -> bool:
        try:
            cls.parse(nsid)
            return True
        except InvalidNsidError:
            return False

    @validator("segments", pre=True, always=True)
    def validate_segments(cls, nsid):
        if isinstance(nsid, str):
            ensure_valid_nsid(nsid)
            segments = nsid.split('.')
            return segments
        return nsid

    @property
    def authority(self):
        return '.'.join(self.segments[:-1][::-1])

    @property
    def name(self):
        return self.segments[-1]

    def __str__(self):
        return '.'.join(self.segments)



class InvalidNsidError(Exception):
    pass


def ensure_valid_nsid(nsid: str) -> None:
    split = nsid.split(".")
    to_check = ".".join(split[:-1]) if split[-1] == "*" else ".".join(split)

    if not re.match(r"^[a-zA-Z0-9.-]*$", to_check):
        raise InvalidNsidError(
            "Disallowed characters in NSID (ASCII letters, digits, dashes, periods only)"
        )

    if len(to_check) > 253 + 1 + 128:
        raise InvalidNsidError("NSID is too long (382 chars max)")

    labels = to_check.split(".")
    if len(split) < 3:
        raise InvalidNsidError("NSID needs at least three parts")

    for i, l in enumerate(labels):
        if len(l) < 1:
            raise InvalidNsidError("NSID parts can not be empty")

        if len(l) > 63 and i + 1 < len(labels):
            raise InvalidNsidError("NSID domain part too long (max 63 chars)")

        if len(l) > 128 and i + 1 == len(labels):
            raise InvalidNsidError("NSID name part too long (max 127 chars)")

        if l.endswith("-"):
            raise InvalidNsidError("NSID parts can not end with hyphen")

        if not re.match(r"^[a-zA-Z]", l):
            raise InvalidNsidError("NSID parts must start with ASCII letter")


def ensure_valid_nsid_regex(nsid: str) -> None:
    if not re.match(
        (
            r"^[a-zA-Z]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?"
            r"(\.[a-zA-Z]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)+"
            r"(\.[a-zA-Z]([a-zA-Z0-9-]{0,126}[a-zA-Z0-9])?)$"
        ),
        nsid,
    ):
        raise InvalidNsidError("NSID didn't validate via regex")

    if len(nsid) > 253 + 1 + 128:
        raise InvalidNsidError("NSID is too long (382 chars max)")
