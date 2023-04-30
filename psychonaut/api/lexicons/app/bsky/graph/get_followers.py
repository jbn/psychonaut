from typing import Any, Optional
from psychonaut.api.lexicons.app.bsky.actor.defs import ProfileView
from psychonaut.api.session import Session
from pydantic import BaseModel, Field
from psychonaut.lexicon.formats import validate_at_identifier


class GetFollowersResp(BaseModel):
    subject: ProfileView
    cursor: Optional[str] = Field(default=None)
    followers: Any


class GetFollowersReq(BaseModel):
    """
    Who is following an actor?
    """

    actor: str = Field(..., pre=True, validator=validate_at_identifier)
    limit: Optional[int] = Field(default=50, ge=1, le=100)
    cursor: Optional[str] = Field(default=None)

    @property
    def xrpc_id(self) -> str:
        return "app.bsky.graph.getFollowers"

    async def do_xrpc(self, sess: Session) -> GetFollowersResp:
        resp = await sess.query(self)
        return GetFollowersResp(**resp)
