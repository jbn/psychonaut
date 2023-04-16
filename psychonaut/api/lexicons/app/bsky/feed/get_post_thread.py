from pydantic import BaseModel, Field
from psychonaut.lexicon.formats import validate_at_uri
from psychonaut.api.session import Session
from typing import Optional, Any


class GetPostThreadReq(BaseModel):
    uri: str = Field(..., pre=True, validator=validate_at_uri)
    depth: Optional[int] = Field(default=None)

    @property
    def xrpc_id(self) -> str:
       return "app.bsky.feed.getPostThread"


class GetPostThreadResp(BaseModel):
    thread: Any

    @property
    def xrpc_id(self) -> str:
       return "app.bsky.feed.getPostThread"


async def get_post_thread(sess: Session, req: GetPostThreadReq) -> GetPostThreadResp:
    resp = await sess.query(req)
    return GetPostThreadResp(**resp)
