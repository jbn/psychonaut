from typing import Any, Optional
from psychonaut.api.lexicons.app.bsky.actor.defs import ProfileView
from psychonaut.api.session import Session
from pydantic import BaseModel, Field
from psychonaut.lexicon.formats import validate_at_identifier


class GetFollowsResp(BaseModel):
    subject: ProfileView
    cursor: Optional[str] = Field(default=None)
    follows: Any


class GetFollowsReq(BaseModel):
    """
    Who is an actor following?
    """

    actor: str = Field(..., pre=True, validator=validate_at_identifier)
    limit: Optional[int] = Field(default=50, ge=1, le=100)
    cursor: Optional[str] = Field(default=None)

    @property
    def xrpc_id(self) -> str:
        return "app.bsky.graph.getFollows"

    async def do_xrpc(self, sess: Session) -> GetFollowsResp:
        resp = await sess.query(self)
        return GetFollowsResp(**resp)
