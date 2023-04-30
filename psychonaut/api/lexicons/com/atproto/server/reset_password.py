from typing import Any
from psychonaut.api.session import Session
from pydantic import BaseModel, Field


class ResetPasswordReq(BaseModel):
    """
    Reset a user account password using a token.
    """

    token: str = Field(...)
    password: str = Field(...)

    @property
    def xrpc_id(self) -> str:
        return "com.atproto.server.resetPassword"

    async def do_xrpc(self, sess: Session) -> Any:
        return await sess.procedure(self)
