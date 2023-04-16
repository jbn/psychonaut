from pydantic import BaseModel, Field
from psychonaut.lexicon.formats import validate_at_uri, validate_cid
from psychonaut.api.session import Session
from typing import Optional, Any


class GetRepostedByReq(BaseModel):
    uri: str = Field(..., pre=True, validator=validate_at_uri)
    cid: Optional[str] = Field(default=None, pre=True, validator=validate_cid)
    limit: Optional[int] = Field(default=50, ge=1, le=100)
    cursor: Optional[str] = Field(default=None)

    @property
    def xrpc_id(self) -> str:
       return "app.bsky.feed.getRepostedBy"


class GetRepostedByResp(BaseModel):
    uri: str = Field(..., pre=True, validator=validate_at_uri)
    cid: Optional[str] = Field(default=None, pre=True, validator=validate_cid)
    cursor: Optional[str] = Field(default=None)
    repostedBy: Any

    @property
    def xrpc_id(self) -> str:
       return "app.bsky.feed.getRepostedBy"


async def get_reposted_by(sess: Session, req: GetRepostedByReq) -> GetRepostedByResp:
    resp = await sess.query(req)
    return GetRepostedByResp(**resp)
