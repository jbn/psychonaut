from typing import Any
from psychonaut.api.session import Session
from pydantic import BaseModel, Field
from psychonaut.lexicon.formats import validate_did


class GetRepoReq(BaseModel):
    """
    View details about a repository.
    """

    did: str = Field(..., pre=True, validator=validate_did)

    @property
    def xrpc_id(self) -> str:
        return "com.atproto.admin.getRepo"

    async def do_xrpc(self, sess: Session) -> Any:
        return await sess.query(self)
