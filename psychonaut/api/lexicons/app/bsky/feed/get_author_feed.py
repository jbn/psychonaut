from typing import Any, Optional
from psychonaut.api.lexicons.app.bsky.feed.defs import FeedViewPost
from psychonaut.api.session import Session
from pydantic import BaseModel, Field
from psychonaut.lexicon.formats import validate_at_identifier


class GetAuthorFeedResp(BaseModel):
    cursor: Optional[str] = Field(default=None)
    feed: Any


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

    async def do_xrpc(self, sess: Session) -> GetAuthorFeedResp:
        resp = await sess.query(self)
        return GetAuthorFeedResp(**resp)
