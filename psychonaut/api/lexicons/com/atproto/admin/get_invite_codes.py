from typing import Any, Optional
from psychonaut.api.lexicons.com.atproto.server.defs import InviteCode
from psychonaut.api.session import Session
from pydantic import BaseModel, Field


class GetInviteCodesResp(BaseModel):
    cursor: Optional[str] = Field(default=None)
    codes: Any


class GetInviteCodesReq(BaseModel):
    """
    Admin view of invite codes
    """

    sort: Optional[str] = Field(default="recent", known_values=["recent", "usage"])
    limit: Optional[int] = Field(default=100, ge=1, le=500)
    cursor: Optional[str] = Field(default=None)

    @property
    def xrpc_id(self) -> str:
        return "com.atproto.admin.getInviteCodes"

    async def do_xrpc(self, sess: Session) -> GetInviteCodesResp:
        resp = await sess.query(self)
        return GetInviteCodesResp(**resp)
