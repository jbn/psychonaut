from typing import Any, Optional
from pydantic import BaseModel, Field
from psychonaut.lexicon.formats import validate_cid, validate_did
from psychonaut.api.session import Session


class Repo(BaseModel):
    """
    [none provided by spec]
    """

    did: str = Field(..., pre=True, validator=validate_did)
    head: str = Field(..., pre=True, validator=validate_cid)


class ListReposResp(BaseModel):
    cursor: Optional[str] = Field(default=None)
    repos: Any


class ListReposReq(BaseModel):
    """
    List dids and root cids of hosted repos
    """

    limit: Optional[int] = Field(default=500, ge=1, le=1000)
    cursor: Optional[str] = Field(default=None)

    @property
    def xrpc_id(self) -> str:
        return "com.atproto.sync.listRepos"

    async def do_xrpc(self, sess: Session) -> ListReposResp:
        resp = await sess.query(self)
        return ListReposResp(**resp)
