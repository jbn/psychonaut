from typing import Any
from psychonaut.api.session import Session
from pydantic import BaseModel, Field
from psychonaut.lexicon.formats import validate_did


class DeleteAccountReq(BaseModel):
    """
    Delete a user account with a token and password.
    """

    did: str = Field(..., pre=True, validator=validate_did)
    password: str = Field(...)
    token: str = Field(...)

    @property
    def xrpc_id(self) -> str:
        return "com.atproto.server.deleteAccount"

    async def do_xrpc(self, sess: Session) -> Any:
        return await sess.procedure(self)
