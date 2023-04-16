from pydantic import BaseModel, Field
from psychonaut.api.session import Session
from typing import Optional, Any


class ListReposReq(BaseModel):
    """
    List dids and root cids of hosted repos
    """
    limit: Optional[int] = Field(default=500, ge=1, le=1000)
    cursor: Optional[str] = Field(default=None)

    @property
    def xrpc_id(self) -> str:
       return "com.atproto.sync.listRepos"


class ListReposResp(BaseModel):
    cursor: Optional[str] = Field(default=None)
    repos: Any

    @property
    def xrpc_id(self) -> str:
       return "com.atproto.sync.listRepos"


async def list_repos(sess: Session, req: ListReposReq) -> ListReposResp:
    resp = await sess.query(req)
    return ListReposResp(**resp)
