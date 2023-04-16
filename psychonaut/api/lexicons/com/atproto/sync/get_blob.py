from pydantic import BaseModel, Field
from psychonaut.lexicon.formats import validate_did, validate_cid
from psychonaut.api.session import Session
from typing import Optional, Any


class GetBlobReq(BaseModel):
    """
    Get a blob associated with a given repo.
    """
    did: str = Field(..., description='The DID of the repo.', pre=True, validator=validate_did)
    cid: str = Field(..., description='The CID of the blob to fetch', pre=True, validator=validate_cid)

    @property
    def xrpc_id(self) -> str:
       return "com.atproto.sync.getBlob"


async def get_blob(sess: Session, req: GetBlobReq) -> Any:
    return await sess.query(req)
