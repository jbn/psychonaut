from pydantic import BaseModel, Field
from psychonaut.api.session import Session
from typing import Optional, Any


class GetInviteCodesReq(BaseModel):
    """
    Admin view of invite codes
    """
    sort: Optional[str] = Field(default='recent', known_values=['recent', 'usage'])
    limit: Optional[int] = Field(default=100, ge=1, le=500)
    cursor: Optional[str] = Field(default=None)

    @property
    def xrpc_id(self) -> str:
       return "com.atproto.admin.getInviteCodes"


class GetInviteCodesResp(BaseModel):
    cursor: Optional[str] = Field(default=None)
    codes: Any

    @property
    def xrpc_id(self) -> str:
       return "com.atproto.admin.getInviteCodes"


async def get_invite_codes(sess: Session, req: GetInviteCodesReq) -> GetInviteCodesResp:
    resp = await sess.query(req)
    return GetInviteCodesResp(**resp)
