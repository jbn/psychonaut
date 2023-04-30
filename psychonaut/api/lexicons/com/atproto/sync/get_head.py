from typing import Any
from psychonaut.api.session import Session
from pydantic import BaseModel, Field
from psychonaut.lexicon.formats import validate_cid, validate_did


class GetHeadResp(BaseModel):
    root: str = Field(..., pre=True, validator=validate_cid)


class GetHeadReq(BaseModel):
    """
    Gets the current HEAD CID of a repo.
    """

    did: str = Field(
        ..., description="The DID of the repo.", pre=True, validator=validate_did
    )

    @property
    def xrpc_id(self) -> str:
        return "com.atproto.sync.getHead"

    async def do_xrpc(self, sess: Session) -> GetHeadResp:
        resp = await sess.query(self)
        return GetHeadResp(**resp)
