from pydantic import BaseModel, Field
from psychonaut.lexicon.formats import (
    validate_nsid, validate_at_uri, validate_at_identifier, validate_cid
)
from psychonaut.api.session import Session
from typing import Optional, Any


class GetRecordReq(BaseModel):
    """
    Get a record.
    """
    repo: str = Field(..., description='The handle or DID of the repo.', pre=True, validator=validate_at_identifier)
    collection: str = Field(..., description='The NSID of the record collection.', pre=True, validator=validate_nsid)
    rkey: str = Field(..., description='The key of the record.')
    cid: Optional[str] = Field(default=None, description='The CID of the version of the record. If not specified, then return the most recent version.', pre=True, validator=validate_cid)

    @property
    def xrpc_id(self) -> str:
       return "com.atproto.repo.getRecord"


class GetRecordResp(BaseModel):
    uri: str = Field(..., pre=True, validator=validate_at_uri)
    cid: Optional[str] = Field(default=None, pre=True, validator=validate_cid)
    value: Any

    @property
    def xrpc_id(self) -> str:
       return "com.atproto.repo.getRecord"


async def get_record(sess: Session, req: GetRecordReq) -> GetRecordResp:
    resp = await sess.query(req)
    return GetRecordResp(**resp)
