from pydantic import BaseModel, Field
from psychonaut.api.session import Session
from typing import Optional, Any


class GetPopularReq(BaseModel):
    """
    An unspecced view of globally popular items
    """
    limit: Optional[int] = Field(default=50, ge=1, le=100)
    cursor: Optional[str] = Field(default=None)

    @property
    def xrpc_id(self) -> str:
       return "app.bsky.unspecced.getPopular"


class GetPopularResp(BaseModel):
    cursor: Optional[str] = Field(default=None)
    feed: Any

    @property
    def xrpc_id(self) -> str:
       return "app.bsky.unspecced.getPopular"


async def get_popular(sess: Session, req: GetPopularReq) -> GetPopularResp:
    resp = await sess.query(req)
    return GetPopularResp(**resp)
