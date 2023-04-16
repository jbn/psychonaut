from pydantic import BaseModel, Field
from psychonaut.api.session import Session
from typing import Optional, Any


class GetModerationActionReq(BaseModel):
    """
    View details about a moderation action.
    """
    id: int = Field(...)

    @property
    def xrpc_id(self) -> str:
       return "com.atproto.admin.getModerationAction"


async def get_moderation_action(sess: Session, req: GetModerationActionReq) -> Any:
    return await sess.query(req)
