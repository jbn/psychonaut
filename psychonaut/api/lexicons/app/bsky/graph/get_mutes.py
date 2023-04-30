from typing import Any, Optional
from psychonaut.api.lexicons.app.bsky.actor.defs import ProfileView
from psychonaut.api.session import Session
from pydantic import BaseModel, Field


class GetMutesResp(BaseModel):
    cursor: Optional[str] = Field(default=None)
    mutes: Any


class GetMutesReq(BaseModel):
    """
    Who does the viewer mute?
    """

    limit: Optional[int] = Field(default=50, ge=1, le=100)
    cursor: Optional[str] = Field(default=None)

    @property
    def xrpc_id(self) -> str:
        return "app.bsky.graph.getMutes"

    async def do_xrpc(self, sess: Session) -> GetMutesResp:
        resp = await sess.query(self)
        return GetMutesResp(**resp)
