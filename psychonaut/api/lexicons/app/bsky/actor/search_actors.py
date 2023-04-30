from typing import Any, Optional
from psychonaut.api.lexicons.app.bsky.actor.defs import ProfileView
from psychonaut.api.session import Session
from pydantic import BaseModel, Field


class SearchActorsResp(BaseModel):
    cursor: Optional[str] = Field(default=None)
    actors: Any


class SearchActorsReq(BaseModel):
    """
    Find actors matching search criteria.
    """

    term: Optional[str] = Field(default=None)
    limit: Optional[int] = Field(default=50, ge=1, le=100)
    cursor: Optional[str] = Field(default=None)

    @property
    def xrpc_id(self) -> str:
        return "app.bsky.actor.searchActors"

    async def do_xrpc(self, sess: Session) -> SearchActorsResp:
        resp = await sess.query(self)
        return SearchActorsResp(**resp)
