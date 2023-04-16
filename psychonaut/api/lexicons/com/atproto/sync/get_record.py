from pydantic import BaseModel, Field
from psychonaut.lexicon.formats import (
    validate_did, validate_nsid, validate_cid
)
from psychonaut.api.session import Session
from typing import Optional, Any


class GetRecordReq(BaseModel):
    """
    Gets blocks needed for existence or non-existence of record.
    """
    did: str = Field(..., description='The DID of the repo.', pre=True, validator=validate_did)
    collection: str = Field(..., pre=True, validator=validate_nsid)
    rkey: str = Field(...)
    commit: Optional[str] = Field(default=None, description='An optional past commit CID.', pre=True, validator=validate_cid)

    @property
    def xrpc_id(self) -> str:
       return "com.atproto.sync.getRecord"


async def get_record(sess: Session, req: GetRecordReq) -> Any:
    return await sess.query(req)
