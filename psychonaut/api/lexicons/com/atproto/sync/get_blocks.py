from typing import Any, Optional, List
from psychonaut.api.session import Session
from pydantic import BaseModel, Field
from psychonaut.lexicon.formats import validate_cid, validate_did, validate_array


class GetBlocksReq(BaseModel):
    """
    Gets blocks from a given repo.
    """

    did: str = Field(
        ..., description="The DID of the repo.", pre=True, validator=validate_did
    )
    cids: List[str] = Field(..., pre=True, validator=validate_array(validate_cid))

    @property
    def xrpc_id(self) -> str:
        return "com.atproto.sync.getBlocks"

    async def do_xrpc(self, sess: Session) -> Any:
        return await sess.query(self)
