from typing import Any, Optional
from psychonaut.api.lexicons.app.bsky.actor.defs import ProfileView
from psychonaut.api.session import Session
from pydantic import BaseModel, Field


class GetBlocksResp(BaseModel):
    cursor: Optional[str] = Field(default=None)
    blocks: Any


class GetBlocksReq(BaseModel):
    """
    Who is the requester's account blocking?
    """

    limit: Optional[int] = Field(default=50, ge=1, le=100)
    cursor: Optional[str] = Field(default=None)

    @property
    def xrpc_id(self) -> str:
        return "app.bsky.graph.getBlocks"

    async def do_xrpc(self, sess: Session) -> GetBlocksResp:
        resp = await sess.query(self)
        return GetBlocksResp(**resp)
