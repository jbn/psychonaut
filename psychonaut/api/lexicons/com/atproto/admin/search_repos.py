from typing import Any, Optional
from psychonaut.api.lexicons.com.atproto.admin.defs import RepoView
from psychonaut.api.session import Session
from pydantic import BaseModel, Field


class SearchReposResp(BaseModel):
    cursor: Optional[str] = Field(default=None)
    repos: Any


class SearchReposReq(BaseModel):
    """
    Find repositories based on a search term.
    """

    term: Optional[str] = Field(default=None)
    invitedBy: Optional[str] = Field(default=None)
    limit: Optional[int] = Field(default=50, ge=1, le=100)
    cursor: Optional[str] = Field(default=None)

    @property
    def xrpc_id(self) -> str:
        return "com.atproto.admin.searchRepos"

    async def do_xrpc(self, sess: Session) -> SearchReposResp:
        resp = await sess.query(self)
        return SearchReposResp(**resp)
