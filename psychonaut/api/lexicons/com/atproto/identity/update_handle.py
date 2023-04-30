from typing import Any
from psychonaut.api.session import Session
from pydantic import BaseModel, Field
from psychonaut.lexicon.formats import validate_handle


class UpdateHandleReq(BaseModel):
    """
    Updates the handle of the account
    """

    handle: str = Field(..., pre=True, validator=validate_handle)

    @property
    def xrpc_id(self) -> str:
        return "com.atproto.identity.updateHandle"

    async def do_xrpc(self, sess: Session) -> Any:
        return await sess.procedure(self)
