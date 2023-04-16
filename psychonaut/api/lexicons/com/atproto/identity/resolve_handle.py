from pydantic import BaseModel, Field
from psychonaut.lexicon.formats import validate_did, validate_handle
from psychonaut.api.session import Session
from typing import Optional, Any


class ResolveHandleReq(BaseModel):
    """
    Provides the DID of a repo.
    """
    handle: Optional[str] = Field(default=None, description="The handle to resolve. If not supplied, will resolve the host's own handle.", pre=True, validator=validate_handle)

    @property
    def xrpc_id(self) -> str:
       return "com.atproto.identity.resolveHandle"


class ResolveHandleResp(BaseModel):
    did: str = Field(..., pre=True, validator=validate_did)

    @property
    def xrpc_id(self) -> str:
       return "com.atproto.identity.resolveHandle"


async def resolve_handle(sess: Session, req: ResolveHandleReq) -> ResolveHandleResp:
    resp = await sess.query(req)
    return ResolveHandleResp(**resp)
