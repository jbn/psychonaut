from typing import Any, Optional
from psychonaut.api.lexicons.app.bsky.feed.defs import FeedViewPost
from psychonaut.api.session import Session
from pydantic import BaseModel, Field


class GetTimelineResp(BaseModel):
    cursor: Optional[str] = Field(default=None)
    feed: Any


class GetTimelineReq(BaseModel):
    """
    A view of the user's home timeline.
    """

    algorithm: Optional[str] = Field(default=None)
    limit: Optional[int] = Field(default=50, ge=1, le=100)
    cursor: Optional[str] = Field(default=None)

    @property
    def xrpc_id(self) -> str:
        return "app.bsky.feed.getTimeline"

    async def do_xrpc(self, sess: Session) -> GetTimelineResp:
        resp = await sess.query(self)
        return GetTimelineResp(**resp)
