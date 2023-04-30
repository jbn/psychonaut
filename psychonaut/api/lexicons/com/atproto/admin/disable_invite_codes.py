from typing import Any, Optional, List
from psychonaut.api.session import Session
from pydantic import BaseModel, Field


class DisableInviteCodesReq(BaseModel):
    """
    Disable some set of codes and/or all codes associated with a set of
    users
    """

    codes: Optional[List[str]] = Field(default=None)
    accounts: Optional[List[str]] = Field(default=None)

    @property
    def xrpc_id(self) -> str:
        return "com.atproto.admin.disableInviteCodes"

    async def do_xrpc(self, sess: Session) -> Any:
        return await sess.procedure(self)
