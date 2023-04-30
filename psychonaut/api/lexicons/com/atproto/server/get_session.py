from typing import Any, Optional
from psychonaut.api.session import Session
from pydantic import BaseModel, Field
from psychonaut.lexicon.formats import validate_did, validate_handle


class GetSessionResp(BaseModel):
    handle: str = Field(..., pre=True, validator=validate_handle)
    did: str = Field(..., pre=True, validator=validate_did)
    email: Optional[str] = Field(default=None)


class GetSessionReq(BaseModel):
    """
    Get information about the current session.
    """

    @property
    def xrpc_id(self) -> str:
        return "com.atproto.server.getSession"

    async def do_xrpc(self, sess: Session) -> GetSessionResp:
        resp = await sess.query(self)
        return GetSessionResp(**resp)
