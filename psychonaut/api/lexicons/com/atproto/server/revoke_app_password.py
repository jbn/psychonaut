from typing import Any
from psychonaut.api.session import Session
from pydantic import BaseModel, Field


class RevokeAppPasswordReq(BaseModel):
    """
    Revoke an app-specific password by name.
    """

    name: str = Field(...)

    @property
    def xrpc_id(self) -> str:
        return "com.atproto.server.revokeAppPassword"

    async def do_xrpc(self, sess: Session) -> Any:
        return await sess.procedure(self)
