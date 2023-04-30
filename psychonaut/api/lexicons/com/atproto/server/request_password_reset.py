from typing import Any
from psychonaut.api.session import Session
from pydantic import BaseModel, Field


class RequestPasswordResetReq(BaseModel):
    """
    Initiate a user account password reset via email.
    """

    email: str = Field(...)

    @property
    def xrpc_id(self) -> str:
        return "com.atproto.server.requestPasswordReset"

    async def do_xrpc(self, sess: Session) -> Any:
        return await sess.procedure(self)
