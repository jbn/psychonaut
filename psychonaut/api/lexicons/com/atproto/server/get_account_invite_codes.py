from typing import Any, Optional
from psychonaut.api.lexicons.com.atproto.server.defs import InviteCode
from psychonaut.api.session import Session
from pydantic import BaseModel, Field


class GetAccountInviteCodesResp(BaseModel):
    codes: Any


class GetAccountInviteCodesReq(BaseModel):
    """
    Get all invite codes for a given account
    """

    includeUsed: Optional[bool] = Field(default=True)
    createAvailable: Optional[bool] = Field(default=True)

    @property
    def xrpc_id(self) -> str:
        return "com.atproto.server.getAccountInviteCodes"

    async def do_xrpc(self, sess: Session) -> GetAccountInviteCodesResp:
        resp = await sess.query(self)
        return GetAccountInviteCodesResp(**resp)
