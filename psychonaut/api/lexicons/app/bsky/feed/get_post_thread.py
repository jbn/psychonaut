from typing import Any, Optional
from psychonaut.api.lexicons.app.bsky.feed.defs import (
    ThreadViewPost,
    BlockedPost,
    NotFoundPost,
)
from psychonaut.api.session import Session
from pydantic import BaseModel, Field
from psychonaut.lexicon.formats import validate_at_uri


class GetPostThreadResp(BaseModel):
    thread: Any


class GetPostThreadReq(BaseModel):
    """
    [none provided by spec]
    """

    uri: str = Field(..., pre=True, validator=validate_at_uri)
    depth: Optional[int] = Field(default=None)

    @property
    def xrpc_id(self) -> str:
        return "app.bsky.feed.getPostThread"

    async def do_xrpc(self, sess: Session) -> GetPostThreadResp:
        resp = await sess.query(self)
        return GetPostThreadResp(**resp)
