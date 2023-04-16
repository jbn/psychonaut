from pydantic import BaseModel, Field
from psychonaut.lexicon.formats import (
    validate_did, validate_array, validate_cid
)
from typing import Optional, List, Any
from psychonaut.api.session import Session


class GetBlocksReq(BaseModel):
    """
    Gets blocks from a given repo.
    """
    did: str = Field(..., description='The DID of the repo.', pre=True, validator=validate_did)
    cids: List[str] = Field(..., pre=True, validator=validate_array(validate_cid))

    @property
    def xrpc_id(self) -> str:
       return "com.atproto.sync.getBlocks"


async def get_blocks(sess: Session, req: GetBlocksReq) -> Any:
    return await sess.query(req)
