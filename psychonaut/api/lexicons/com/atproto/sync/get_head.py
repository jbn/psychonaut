from pydantic import BaseModel, Field
from psychonaut.lexicon.formats import validate_did, validate_cid
from psychonaut.api.session import Session
from typing import Optional, Any


class GetHeadReq(BaseModel):
    """
    Gets the current HEAD CID of a repo.
    """
    did: str = Field(..., description='The DID of the repo.', pre=True, validator=validate_did)

    @property
    def xrpc_id(self) -> str:
       return "com.atproto.sync.getHead"


class GetHeadResp(BaseModel):
    root: str = Field(..., pre=True, validator=validate_cid)

    @property
    def xrpc_id(self) -> str:
       return "com.atproto.sync.getHead"


async def get_head(sess: Session, req: GetHeadReq) -> GetHeadResp:
    resp = await sess.query(req)
    return GetHeadResp(**resp)
