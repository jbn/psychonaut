from typing import Any, Optional
from psychonaut.api.lexicons.app.bsky.actor.defs import ProfileViewBasic
from psychonaut.api.session import Session
from pydantic import BaseModel, Field


class SearchActorsTypeaheadResp(BaseModel):
    actors: Any


class SearchActorsTypeaheadReq(BaseModel):
    """
    Find actor suggestions for a search term.
    """

    term: Optional[str] = Field(default=None)
    limit: Optional[int] = Field(default=50, ge=1, le=100)

    @property
    def xrpc_id(self) -> str:
        return "app.bsky.actor.searchActorsTypeahead"

    async def do_xrpc(self, sess: Session) -> SearchActorsTypeaheadResp:
        resp = await sess.query(self)
        return SearchActorsTypeaheadResp(**resp)
