from pydantic import BaseModel, Field
from psychonaut.api.session import Session
from typing import Optional, Any


class GetAccountInviteCodesReq(BaseModel):
    """
    Get all invite codes for a given account
    """
    includeUsed: Optional[bool] = Field(default=True)
    createAvailable: Optional[bool] = Field(default=True)

    @property
    def xrpc_id(self) -> str:
       return "com.atproto.server.getAccountInviteCodes"


class GetAccountInviteCodesResp(BaseModel):
    codes: Any

    @property
    def xrpc_id(self) -> str:
       return "com.atproto.server.getAccountInviteCodes"


async def get_account_invite_codes(sess: Session, req: GetAccountInviteCodesReq) -> GetAccountInviteCodesResp:
    resp = await sess.query(req)
    return GetAccountInviteCodesResp(**resp)
