from pydantic import BaseModel, Field
from psychonaut.api.session import Session
from typing import Optional, Any


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


class GetModerationActionsResp(BaseModel):
    cursor: Optional[str] = Field(default=None)
    actions: Any

    @property
    def xrpc_id(self) -> str:
       return "com.atproto.admin.getModerationActions"


async def get_moderation_actions(sess: Session, req: GetModerationActionsReq) -> GetModerationActionsResp:
    resp = await sess.query(req)
    return GetModerationActionsResp(**resp)
