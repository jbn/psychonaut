from typing import Any
from psychonaut.api.session import Session
from pydantic import BaseModel, Field
from psychonaut.lexicon.formats import validate_handle, validate_did


class UpdateAccountHandleReq(BaseModel):
    """
    Administrative action to update an account's handle
    """

    did: str = Field(..., pre=True, validator=validate_did)
    handle: str = Field(..., pre=True, validator=validate_handle)

    @property
    def xrpc_id(self) -> str:
        return "com.atproto.admin.updateAccountHandle"

    async def do_xrpc(self, sess: Session) -> Any:
        return await sess.procedure(self)
