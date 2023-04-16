from pydantic import BaseModel, Field
from psychonaut.lexicon.formats import validate_did, validate_handle
from psychonaut.api.session import Session
from typing import Optional, Any


class GetSessionReq(BaseModel):
    """
    Get information about the current session.
    """

    @property
    def xrpc_id(self) -> str:
       return "com.atproto.server.getSession"


class GetSessionResp(BaseModel):
    handle: str = Field(..., pre=True, validator=validate_handle)
    did: str = Field(..., pre=True, validator=validate_did)
    email: Optional[str] = Field(default=None)

    @property
    def xrpc_id(self) -> str:
       return "com.atproto.server.getSession"


async def get_session(sess: Session, req: GetSessionReq) -> GetSessionResp:
    resp = await sess.query(req)
    return GetSessionResp(**resp)
