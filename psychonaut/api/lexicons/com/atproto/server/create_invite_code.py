from typing import Any, Optional
from psychonaut.api.session import Session
from pydantic import BaseModel, Field
from psychonaut.lexicon.formats import validate_did


class CreateInviteCodeResp(BaseModel):
    code: str = Field(...)


class CreateInviteCodeReq(BaseModel):
    """
    Create an invite code.
    """

    useCount: int = Field(...)
    forAccount: Optional[str] = Field(default=None, pre=True, validator=validate_did)

    @property
    def xrpc_id(self) -> str:
        return "com.atproto.server.createInviteCode"

    async def do_xrpc(self, sess: Session) -> CreateInviteCodeResp:
        resp = await sess.procedure(self)
        return CreateInviteCodeResp(**resp)
