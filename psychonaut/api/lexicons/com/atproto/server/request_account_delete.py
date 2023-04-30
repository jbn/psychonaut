from typing import Any
from psychonaut.api.session import Session
from pydantic import BaseModel


class RequestAccountDeleteReq(BaseModel):
    """
    Initiate a user account deletion via email.
    """

    @property
    def xrpc_id(self) -> str:
        return "com.atproto.server.requestAccountDelete"

    async def do_xrpc(self, sess: Session) -> Any:
        return await sess.procedure(self)
