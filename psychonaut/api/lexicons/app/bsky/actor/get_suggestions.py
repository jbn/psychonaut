from pydantic import BaseModel, Field
from psychonaut.api.session import Session
from typing import Optional, Any


class GetSuggestionsReq(BaseModel):
    """
    Get a list of actors suggested for following. Used in discovery UIs.
    """
    limit: Optional[int] = Field(default=50, ge=1, le=100)
    cursor: Optional[str] = Field(default=None)

    @property
    def xrpc_id(self) -> str:
       return "app.bsky.actor.getSuggestions"


class GetSuggestionsResp(BaseModel):
    cursor: Optional[str] = Field(default=None)
    actors: Any

    @property
    def xrpc_id(self) -> str:
       return "app.bsky.actor.getSuggestions"


async def get_suggestions(sess: Session, req: GetSuggestionsReq) -> GetSuggestionsResp:
    resp = await sess.query(req)
    return GetSuggestionsResp(**resp)
