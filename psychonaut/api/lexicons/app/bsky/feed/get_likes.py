from pydantic import BaseModel, Field
from psychonaut.lexicon.formats import validate_at_uri, validate_cid
from psychonaut.api.session import Session
from typing import Optional, Any


class GetLikesReq(BaseModel):
    uri: str = Field(..., pre=True, validator=validate_at_uri)
    cid: Optional[str] = Field(default=None, pre=True, validator=validate_cid)
    limit: Optional[int] = Field(default=50, ge=1, le=100)
    cursor: Optional[str] = Field(default=None)

    @property
    def xrpc_id(self) -> str:
       return "app.bsky.feed.getLikes"


class GetLikesResp(BaseModel):
    uri: str = Field(..., pre=True, validator=validate_at_uri)
    cid: Optional[str] = Field(default=None, pre=True, validator=validate_cid)
    cursor: Optional[str] = Field(default=None)
    likes: Any

    @property
    def xrpc_id(self) -> str:
       return "app.bsky.feed.getLikes"


async def get_likes(sess: Session, req: GetLikesReq) -> GetLikesResp:
    resp = await sess.query(req)
    return GetLikesResp(**resp)
