from typing import Any, Optional
from psychonaut.api.lexicons.app.bsky.actor.defs import ProfileView
from pydantic import BaseModel, Field
from psychonaut.lexicon.formats import validate_at_uri, validate_cid, validate_datetime
from psychonaut.api.session import Session


class Like(BaseModel):
    """
    [none provided by spec]
    """

    indexedAt: str = Field(..., pre=True, validator=validate_datetime)
    createdAt: str = Field(..., pre=True, validator=validate_datetime)
    actor: ProfileView


class GetLikesResp(BaseModel):
    uri: str = Field(..., pre=True, validator=validate_at_uri)
    cid: Optional[str] = Field(default=None, pre=True, validator=validate_cid)
    cursor: Optional[str] = Field(default=None)
    likes: Any


class GetLikesReq(BaseModel):
    """
    [none provided by spec]
    """

    uri: str = Field(..., pre=True, validator=validate_at_uri)
    cid: Optional[str] = Field(default=None, pre=True, validator=validate_cid)
    limit: Optional[int] = Field(default=50, ge=1, le=100)
    cursor: Optional[str] = Field(default=None)

    @property
    def xrpc_id(self) -> str:
        return "app.bsky.feed.getLikes"

    async def do_xrpc(self, sess: Session) -> GetLikesResp:
        resp = await sess.query(self)
        return GetLikesResp(**resp)
