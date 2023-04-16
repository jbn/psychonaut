from pydantic import BaseModel, Field
from psychonaut.api.session import Session
from typing import Optional, Any


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


class SearchReposResp(BaseModel):
    cursor: Optional[str] = Field(default=None)
    repos: Any

    @property
    def xrpc_id(self) -> str:
       return "com.atproto.admin.searchRepos"


async def search_repos(sess: Session, req: SearchReposReq) -> SearchReposResp:
    resp = await sess.query(req)
    return SearchReposResp(**resp)
