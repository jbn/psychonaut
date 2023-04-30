from typing import Any
from psychonaut.api.session import Session
from pydantic import BaseModel, Field
from psychonaut.lexicon.formats import validate_at_identifier


class MuteActorReq(BaseModel):
    """
    Mute an actor by did or handle.
    """

    actor: str = Field(..., pre=True, validator=validate_at_identifier)

    @property
    def xrpc_id(self) -> str:
        return "app.bsky.graph.muteActor"

    async def do_xrpc(self, sess: Session) -> Any:
        return await sess.procedure(self)
