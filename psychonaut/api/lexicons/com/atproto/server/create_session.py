from typing import Any, Optional
from psychonaut.api.session import Session
from pydantic import BaseModel, Field
from psychonaut.lexicon.formats import validate_did, validate_handle


class CreateSessionResp(BaseModel):
    accessJwt: str = Field(...)
    refreshJwt: str = Field(...)
    handle: str = Field(..., pre=True, validator=validate_handle)
    did: str = Field(..., pre=True, validator=validate_did)
    email: Optional[str] = Field(default=None)


class CreateSessionReq(BaseModel):
    """
    Create an authentication session.
    """

    identifier: str = Field(
        ...,
        description="Handle or other identifier supported by the server for the authenticating user.",
    )
    password: str = Field(...)

    @property
    def xrpc_id(self) -> str:
        return "com.atproto.server.createSession"

    async def do_xrpc(self, sess: Session) -> CreateSessionResp:
        resp = await sess.procedure(self)
        return CreateSessionResp(**resp)
