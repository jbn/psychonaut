"""
See:

https://github.dev/bluesky-social/atproto/blob/main/packages/lexicon/src/validators/formats.ts
"""
import re


class InvalidDidError(ValueError):
    pass


def ensure_valid_did(did: str) -> None:
    # check that all chars are boring ASCII
    if not re.match(r"^[a-zA-Z0-9._:%-]*$", did):
        raise InvalidDidError(
            "Disallowed characters in DID (ASCII letters, digits, and a couple other characters only)"
        )

    parts = did.split(":")
    if len(parts) < 3:
        raise InvalidDidError(
            "DID requires prefix, method, and method-specific content"
        )

    if parts[0] != "did":
        raise InvalidDidError('DID requires "did:" prefix')

    if not re.match(r"^[a-z]+$", parts[1]):
        raise InvalidDidError("DID method must be lower-case letters")

    if did.endswith(":") or did.endswith("%"):
        raise InvalidDidError('DID can not end with ":" or "%"')

    if len(did) > 8 * 1024:
        raise InvalidDidError("DID is far too long")


def ensure_valid_did_regex(did: str) -> None:
    # simple regex to enforce most constraints via just regex and length
    if not re.match(r"^did:[a-z]+:[a-zA-Z0-9._:%-]*[a-zA-Z0-9._-]$", did):
        raise InvalidDidError("DID didn't validate via regex")

    if len(did) > 8 * 1024:
        raise InvalidDidError("DID is far too long")
