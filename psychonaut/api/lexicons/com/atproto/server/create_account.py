from typing import Any, Optional
from psychonaut.api.session import Session
from pydantic import BaseModel, Field
from psychonaut.lexicon.formats import validate_did, validate_handle


class CreateAccountResp(BaseModel):
    accessJwt: str = Field(...)
    refreshJwt: str = Field(...)
    handle: str = Field(..., pre=True, validator=validate_handle)
    did: str = Field(..., pre=True, validator=validate_did)


class CreateAccountReq(BaseModel):
    """
    Create an account.
    """

    email: str = Field(...)
    handle: str = Field(..., pre=True, validator=validate_handle)
    inviteCode: Optional[str] = Field(default=None)
    password: str = Field(...)
    recoveryKey: Optional[str] = Field(default=None)

    @property
    def xrpc_id(self) -> str:
        return "com.atproto.server.createAccount"

    async def do_xrpc(self, sess: Session) -> CreateAccountResp:
        resp = await sess.procedure(self)
        return CreateAccountResp(**resp)
