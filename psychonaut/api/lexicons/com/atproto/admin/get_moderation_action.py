from typing import Any
from psychonaut.api.session import Session
from pydantic import BaseModel, Field


class GetModerationActionReq(BaseModel):
    """
    View details about a moderation action.
    """

    id: int = Field(...)

    @property
    def xrpc_id(self) -> str:
        return "com.atproto.admin.getModerationAction"

    async def do_xrpc(self, sess: Session) -> Any:
        return await sess.query(self)
