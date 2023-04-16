from pydantic import BaseModel, Field
from psychonaut.lexicon.formats import validate_at_identifier
from psychonaut.api.session import Session
from typing import Optional, Any


class GetAuthorFeedReq(BaseModel):
    """
    A view of an actor's feed.
    """
    actor: str = Field(..., pre=True, validator=validate_at_identifier)
    limit: Optional[int] = Field(default=50, ge=1, le=100)
    cursor: Optional[str] = Field(default=None)

    @property
    def xrpc_id(self) -> str:
       return "app.bsky.feed.getAuthorFeed"


class GetAuthorFeedResp(BaseModel):
    cursor: Optional[str] = Field(default=None)
    feed: Any

    @property
    def xrpc_id(self) -> str:
       return "app.bsky.feed.getAuthorFeed"


async def get_author_feed(sess: Session, req: GetAuthorFeedReq) -> GetAuthorFeedResp:
    resp = await sess.query(req)
    return GetAuthorFeedResp(**resp)
