from typing import Any, Optional
from psychonaut.api.session import Session
from pydantic import BaseModel, Field
from psychonaut.lexicon.formats import (
    validate_at_uri,
    validate_cid,
    validate_at_identifier,
    validate_nsid,
)


class GetRecordResp(BaseModel):
    uri: str = Field(..., pre=True, validator=validate_at_uri)
    cid: Optional[str] = Field(default=None, pre=True, validator=validate_cid)
    value: Any


class GetRecordReq(BaseModel):
    """
    Get a record.
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
    cid: Optional[str] = Field(
        default=None,
        description="The CID of the version of the record. If not specified, then return the most recent version.",
        pre=True,
        validator=validate_cid,
    )

    @property
    def xrpc_id(self) -> str:
        return "com.atproto.repo.getRecord"

    async def do_xrpc(self, sess: Session) -> GetRecordResp:
        resp = await sess.query(self)
        return GetRecordResp(**resp)
