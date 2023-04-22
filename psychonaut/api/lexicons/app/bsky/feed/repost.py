from pydantic import BaseModel, Field
from psychonaut.lexicon.formats import validate_datetime
from psychonaut.api.session import Session
from typing import Optional, Any


class RepostReq(BaseModel):
    subject: Any
    createdAt: str = Field(..., pre=True, validator=validate_datetime)

    @property
    def xrpc_id(self) -> str:
       return "app.bsky.feed.repost"


async def repost(sess: Session, req: RepostReq) -> Any:
    return await sess.record(req)