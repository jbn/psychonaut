from pydantic import BaseModel, Field
from psychonaut.lexicon.formats import validate_at_identifier
from psychonaut.api.session import Session
from typing import Optional, Any


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


class GetFollowersResp(BaseModel):
    subject: Any
    cursor: Optional[str] = Field(default=None)
    followers: Any

    @property
    def xrpc_id(self) -> str:
       return "app.bsky.graph.getFollowers"


async def get_followers(sess: Session, req: GetFollowersReq) -> GetFollowersResp:
    resp = await sess.query(req)
    return GetFollowersResp(**resp)
