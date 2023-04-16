from pydantic import BaseModel, Field
from psychonaut.api.session import Session
from typing import Optional, Any


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


class GetTimelineResp(BaseModel):
    cursor: Optional[str] = Field(default=None)
    feed: Any

    @property
    def xrpc_id(self) -> str:
       return "app.bsky.feed.getTimeline"


async def get_timeline(sess: Session, req: GetTimelineReq) -> GetTimelineResp:
    resp = await sess.query(req)
    return GetTimelineResp(**resp)
