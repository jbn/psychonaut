from typing import Any, Optional
from psychonaut.api.lexicons.app.bsky.actor.defs import ProfileView
from psychonaut.api.session import Session
from pydantic import BaseModel, Field
from psychonaut.lexicon.formats import validate_at_uri, validate_cid


class GetRepostedByResp(BaseModel):
    uri: str = Field(..., pre=True, validator=validate_at_uri)
    cid: Optional[str] = Field(default=None, pre=True, validator=validate_cid)
    cursor: Optional[str] = Field(default=None)
    repostedBy: Any


class GetRepostedByReq(BaseModel):
    """
    [none provided by spec]
    """

    uri: str = Field(..., pre=True, validator=validate_at_uri)
    cid: Optional[str] = Field(default=None, pre=True, validator=validate_cid)
    limit: Optional[int] = Field(default=50, ge=1, le=100)
    cursor: Optional[str] = Field(default=None)

    @property
    def xrpc_id(self) -> str:
        return "app.bsky.feed.getRepostedBy"

    async def do_xrpc(self, sess: Session) -> GetRepostedByResp:
        resp = await sess.query(self)
        return GetRepostedByResp(**resp)
