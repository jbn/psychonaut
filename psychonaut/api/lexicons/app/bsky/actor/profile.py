from pydantic import BaseModel, Field
from psychonaut.api.session import Session
from typing import Optional, Any


class ProfileReq(BaseModel):
    displayName: Optional[str] = Field(default=None, max_length=640)
    description: Optional[str] = Field(default=None, max_length=2560)
    avatar: Optional[Any] = None
    banner: Optional[Any] = None

    @property
    def xrpc_id(self) -> str:
       return "app.bsky.actor.profile"


async def profile(sess: Session, req: ProfileReq) -> Any:
    return await sess.record(req)
