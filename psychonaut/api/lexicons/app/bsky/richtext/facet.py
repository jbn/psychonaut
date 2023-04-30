from typing import Any, Optional, List
from pydantic import BaseModel, Field
from psychonaut.lexicon.formats import validate_uri, validate_did


class ByteSlice(BaseModel):
    """
    A text segment. Start is inclusive, end is exclusive. Indices are for
    utf8-encoded strings.
    """

    byteStart: int = Field(..., ge=0)
    byteEnd: int = Field(..., ge=0)


class Mention(BaseModel):
    """
    A facet feature for actor mentions.
    """

    did: str = Field(..., pre=True, validator=validate_did)


class Link(BaseModel):
    """
    A facet feature for links.
    """

    uri: str = Field(..., pre=True, validator=validate_uri)


class Facet(BaseModel):
    """
    [none provided by spec]
    """

    index: ByteSlice
    features: List[Any] = Field(...)
