from typing import Any, Optional, List
from psychonaut.api.lexicons.app.bsky.feed.defs import PostView
from psychonaut.api.session import Session
from pydantic import BaseModel, Field
from psychonaut.lexicon.formats import validate_at_uri, validate_array


class GetPostsResp(BaseModel):
    posts: Any


class GetPostsReq(BaseModel):
    """
    A view of an actor's feed.
    """

    uris: List[str] = Field(
        ..., max_items=25, pre=True, validator=validate_array(validate_at_uri)
    )

    @property
    def xrpc_id(self) -> str:
        return "app.bsky.feed.getPosts"

    async def do_xrpc(self, sess: Session) -> GetPostsResp:
        resp = await sess.query(self)
        return GetPostsResp(**resp)
