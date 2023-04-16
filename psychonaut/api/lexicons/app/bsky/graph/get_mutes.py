from pydantic import BaseModel, Field
from psychonaut.api.session import Session
from typing import Optional, Any


class GetMutesReq(BaseModel):
    """
    Who does the viewer mute?
    """
    limit: Optional[int] = Field(default=50, ge=1, le=100)
    cursor: Optional[str] = Field(default=None)

    @property
    def xrpc_id(self) -> str:
       return "app.bsky.graph.getMutes"


class GetMutesResp(BaseModel):
    cursor: Optional[str] = Field(default=None)
    mutes: Any

    @property
    def xrpc_id(self) -> str:
       return "app.bsky.graph.getMutes"


async def get_mutes(sess: Session, req: GetMutesReq) -> GetMutesResp:
    resp = await sess.query(req)
    return GetMutesResp(**resp)
