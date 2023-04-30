from typing import Any
from psychonaut.api.session import Session
from pydantic import BaseModel, Field
from psychonaut.lexicon.formats import validate_did


class ReverseModerationActionReq(BaseModel):
    """
    Reverse a moderation action.
    """

    id: int = Field(...)
    reason: str = Field(...)
    createdBy: str = Field(..., pre=True, validator=validate_did)

    @property
    def xrpc_id(self) -> str:
        return "com.atproto.admin.reverseModerationAction"

    async def do_xrpc(self, sess: Session) -> Any:
        return await sess.procedure(self)
