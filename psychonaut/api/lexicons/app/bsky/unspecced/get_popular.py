from typing import Any, Optional
from psychonaut.api.lexicons.app.bsky.feed.defs import FeedViewPost
from psychonaut.api.session import Session
from pydantic import BaseModel, Field


class GetPopularResp(BaseModel):
    cursor: Optional[str] = Field(default=None)
    feed: Any


class GetPopularReq(BaseModel):
    """
    An unspecced view of globally popular items
    """

    limit: Optional[int] = Field(default=50, ge=1, le=100)
    cursor: Optional[str] = Field(default=None)

    @property
    def xrpc_id(self) -> str:
        return "app.bsky.unspecced.getPopular"

    async def do_xrpc(self, sess: Session) -> GetPopularResp:
        resp = await sess.query(self)
        return GetPopularResp(**resp)
