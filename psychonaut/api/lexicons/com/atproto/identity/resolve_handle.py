from typing import Any, Optional
from psychonaut.api.session import Session
from pydantic import BaseModel, Field
from psychonaut.lexicon.formats import validate_handle, validate_did


class ResolveHandleResp(BaseModel):
    did: str = Field(..., pre=True, validator=validate_did)


class ResolveHandleReq(BaseModel):
    """
    Provides the DID of a repo.
    """

    handle: Optional[str] = Field(
        default=None,
        description="The handle to resolve. If not supplied, will resolve the host's own handle.",
        pre=True,
        validator=validate_handle,
    )

    @property
    def xrpc_id(self) -> str:
        return "com.atproto.identity.resolveHandle"

    async def do_xrpc(self, sess: Session) -> ResolveHandleResp:
        resp = await sess.query(self)
        return ResolveHandleResp(**resp)
