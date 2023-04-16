from pydantic import BaseModel, Field
from psychonaut.api.session import Session
from typing import Optional, Any


class SearchActorsTypeaheadReq(BaseModel):
    """
    Find actor suggestions for a search term.
    """
    term: Optional[str] = Field(default=None)
    limit: Optional[int] = Field(default=50, ge=1, le=100)

    @property
    def xrpc_id(self) -> str:
       return "app.bsky.actor.searchActorsTypeahead"


class SearchActorsTypeaheadResp(BaseModel):
    actors: Any

    @property
    def xrpc_id(self) -> str:
       return "app.bsky.actor.searchActorsTypeahead"


async def search_actors_typeahead(sess: Session, req: SearchActorsTypeaheadReq) -> SearchActorsTypeaheadResp:
    resp = await sess.query(req)
    return SearchActorsTypeaheadResp(**resp)
