from typing import Any
from psychonaut.api.session import Session
from pydantic import BaseModel, Field
from psychonaut.lexicon.formats import validate_datetime


class UpdateSeenReq(BaseModel):
    """
    Notify server that the user has seen notifications.
    """

    seenAt: str = Field(..., pre=True, validator=validate_datetime)

    @property
    def xrpc_id(self) -> str:
        return "app.bsky.notification.updateSeen"

    async def do_xrpc(self, sess: Session) -> Any:
        return await sess.procedure(self)
