from typing import Any, Optional
from psychonaut.api.lexicons.com.atproto.admin.defs import ActionView
from psychonaut.api.session import Session
from pydantic import BaseModel, Field


class GetModerationActionsResp(BaseModel):
    cursor: Optional[str] = Field(default=None)
    actions: Any


class GetModerationActionsReq(BaseModel):
    """
    List moderation actions related to a subject.
    """

    subject: Optional[str] = Field(default=None)
    limit: Optional[int] = Field(default=50, ge=1, le=100)
    cursor: Optional[str] = Field(default=None)

    @property
    def xrpc_id(self) -> str:
        return "com.atproto.admin.getModerationActions"

    async def do_xrpc(self, sess: Session) -> GetModerationActionsResp:
        resp = await sess.query(self)
        return GetModerationActionsResp(**resp)
