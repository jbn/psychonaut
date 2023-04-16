from pydantic import BaseModel, Field
from psychonaut.lexicon.formats import validate_did
from psychonaut.api.session import Session
from typing import Optional, Any


class GetRepoReq(BaseModel):
    """
    View details about a repository.
    """
    did: str = Field(..., pre=True, validator=validate_did)

    @property
    def xrpc_id(self) -> str:
       return "com.atproto.admin.getRepo"


async def get_repo(sess: Session, req: GetRepoReq) -> Any:
    return await sess.query(req)
