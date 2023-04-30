from typing import Any, Optional, List
from pydantic import BaseModel, Field
from psychonaut.api.session import Session
from psychonaut.lexicon.formats import validate_did, validate_array


class AccountCodes(BaseModel):
    """
    [none provided by spec]
    """

    account: str = Field(...)
    codes: List[str] = Field(...)


class CreateInviteCodesResp(BaseModel):
    codes: Any


class CreateInviteCodesReq(BaseModel):
    """
    Create an invite code.
    """

    codeCount: int = Field(default=1)
    useCount: int = Field(...)
    forAccounts: Optional[List[str]] = Field(
        default=None, pre=True, validator=validate_array(validate_did)
    )

    @property
    def xrpc_id(self) -> str:
        return "com.atproto.server.createInviteCodes"

    async def do_xrpc(self, sess: Session) -> CreateInviteCodesResp:
        resp = await sess.procedure(self)
        return CreateInviteCodesResp(**resp)
