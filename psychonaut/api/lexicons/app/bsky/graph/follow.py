from pydantic import BaseModel, Field
from psychonaut.lexicon.formats import validate_datetime, validate_did
from psychonaut.api.session import Session
from typing import Optional, Any


class FollowReq(BaseModel):
    subject: str = Field(..., pre=True, validator=validate_did)
    createdAt: str = Field(..., pre=True, validator=validate_datetime)

    @property
    def xrpc_id(self) -> str:
       return "app.bsky.graph.follow"


async def follow(sess: Session, req: FollowReq) -> Any:
    return await sess.record(req)
