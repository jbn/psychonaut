from pydantic import BaseModel, Field
from psychonaut.lexicon.formats import validate_did, validate_cid
from psychonaut.api.session import Session
from typing import Optional, Any


class GetCheckoutReq(BaseModel):
    """
    Gets the repo state.
    """
    did: str = Field(..., description='The DID of the repo.', pre=True, validator=validate_did)
    commit: Optional[str] = Field(default=None, description='The commit to get the checkout from. Defaults to current HEAD.', pre=True, validator=validate_cid)

    @property
    def xrpc_id(self) -> str:
       return "com.atproto.sync.getCheckout"


async def get_checkout(sess: Session, req: GetCheckoutReq) -> Any:
    return await sess.query(req)
