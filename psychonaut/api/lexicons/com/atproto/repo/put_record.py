from typing import Any, Optional
from psychonaut.api.session import Session
from pydantic import BaseModel, Field
from psychonaut.lexicon.formats import (
    validate_at_uri,
    validate_cid,
    validate_at_identifier,
    validate_nsid,
)


class PutRecordResp(BaseModel):
    uri: str = Field(..., pre=True, validator=validate_at_uri)
    cid: str = Field(..., pre=True, validator=validate_cid)


class PutRecordReq(BaseModel):
    """
    Write a record, creating or updating it as needed.
    """

    repo: str = Field(
        ...,
        description="The handle or DID of the repo.",
        pre=True,
        validator=validate_at_identifier,
    )
    collection: str = Field(
        ...,
        description="The NSID of the record collection.",
        pre=True,
        validator=validate_nsid,
    )
    rkey: str = Field(..., description="The key of the record.")
    validate_flag: Optional[bool] = Field(
        alias="validate", default=True, description="Validate the record?"
    )
    record: Any
    swapRecord: Optional[str] = Field(
        default=None,
        description="Compare and swap with the previous record by cid.",
        pre=True,
        validator=validate_cid,
    )
    swapCommit: Optional[str] = Field(
        default=None,
        description="Compare and swap with the previous commit by cid.",
        pre=True,
        validator=validate_cid,
    )

    @property
    def xrpc_id(self) -> str:
        return "com.atproto.repo.putRecord"

    async def do_xrpc(self, sess: Session) -> PutRecordResp:
        resp = await sess.procedure(self)
        return PutRecordResp(**resp)
