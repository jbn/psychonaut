from typing import Any
from psychonaut.api.session import Session
from pydantic import BaseModel, Field
from psychonaut.lexicon.formats import validate_did, validate_handle


class RefreshSessionResp(BaseModel):
    accessJwt: str = Field(...)
    refreshJwt: str = Field(...)
    handle: str = Field(..., pre=True, validator=validate_handle)
    did: str = Field(..., pre=True, validator=validate_did)


class RefreshSessionReq(BaseModel):
    """
    Refresh an authentication session.
    """

    @property
    def xrpc_id(self) -> str:
        return "com.atproto.server.refreshSession"

    async def do_xrpc(self, sess: Session) -> RefreshSessionResp:
        resp = await sess.procedure(self)
        return RefreshSessionResp(**resp)
