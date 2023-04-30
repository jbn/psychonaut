from typing import Any, Optional
from pydantic import BaseModel, Field
from psychonaut.lexicon.formats import (
    validate_cid,
    validate_uri,
    validate_did,
    validate_datetime,
)


class Label(BaseModel):
    """
    Metadata tag on an atproto resource (eg, repo or record)
    """

    src: str = Field(
        ...,
        description="DID of the actor who created this label",
        pre=True,
        validator=validate_did,
    )
    uri: str = Field(
        ...,
        description="AT URI of the record, repository (account), or other resource which this label applies to",
        pre=True,
        validator=validate_uri,
    )
    cid: Optional[str] = Field(
        default=None,
        description="optionally, CID specifying the specific version of 'uri' resource this label applies to",
        pre=True,
        validator=validate_cid,
    )
    val: str = Field(
        ...,
        description="the short string name of the value or type of this label",
        max_length=128,
    )
    neg: Optional[bool] = Field(
        default=None,
        description="if true, this is a negation label, overwriting a previous label",
    )
    cts: str = Field(
        ...,
        description="timestamp when this label was created",
        pre=True,
        validator=validate_datetime,
    )
