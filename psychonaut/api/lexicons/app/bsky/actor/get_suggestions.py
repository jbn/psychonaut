from typing import Any, Optional
from psychonaut.api.lexicons.app.bsky.actor.defs import ProfileView
from psychonaut.api.session import Session
from pydantic import BaseModel, Field


class GetSuggestionsResp(BaseModel):
    cursor: Optional[str] = Field(default=None)
    actors: Any


class GetSuggestionsReq(BaseModel):
    """
    Get a list of actors suggested for following. Used in discovery UIs.
    """

    limit: Optional[int] = Field(default=50, ge=1, le=100)
    cursor: Optional[str] = Field(default=None)

    @property
    def xrpc_id(self) -> str:
        return "app.bsky.actor.getSuggestions"

    async def do_xrpc(self, sess: Session) -> GetSuggestionsResp:
        resp = await sess.query(self)
        return GetSuggestionsResp(**resp)
