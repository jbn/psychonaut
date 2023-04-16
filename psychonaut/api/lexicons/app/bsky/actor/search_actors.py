from pydantic import BaseModel, Field
from psychonaut.api.session import Session
from typing import Optional, Any


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


class SearchActorsResp(BaseModel):
    cursor: Optional[str] = Field(default=None)
    actors: Any

    @property
    def xrpc_id(self) -> str:
       return "app.bsky.actor.searchActors"


async def search_actors(sess: Session, req: SearchActorsReq) -> SearchActorsResp:
    resp = await sess.query(req)
    return SearchActorsResp(**resp)
