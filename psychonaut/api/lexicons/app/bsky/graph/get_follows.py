from pydantic import BaseModel, Field
from psychonaut.lexicon.formats import validate_at_identifier
from psychonaut.api.session import Session
from typing import Optional, Any


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


class GetFollowsResp(BaseModel):
    subject: Any
    cursor: Optional[str] = Field(default=None)
    follows: Any

    @property
    def xrpc_id(self) -> str:
       return "app.bsky.graph.getFollows"


async def get_follows(sess: Session, req: GetFollowsReq) -> GetFollowsResp:
    resp = await sess.query(req)
    return GetFollowsResp(**resp)
