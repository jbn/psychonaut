from typing import Any
from psychonaut.api.session import Session
from pydantic import BaseModel


class DeleteSessionReq(BaseModel):
    """
    Delete the current session.
    """

    @property
    def xrpc_id(self) -> str:
        return "com.atproto.server.deleteSession"

    async def do_xrpc(self, sess: Session) -> Any:
        return await sess.procedure(self)
