from pydantic import BaseModel, Field
from psychonaut.lexicon.formats import validate_datetime
from psychonaut.api.session import Session
from typing import Optional, Any


class PostReq(BaseModel):
    text: str = Field(..., max_length=3000)
    entities: Optional[Any] = None
    facets: Optional[Any] = None
    reply: Optional[Any] = None
    embed: Optional[Any] = None
    createdAt: str = Field(..., pre=True, validator=validate_datetime)

    @property
    def xrpc_id(self) -> str:
       return "app.bsky.feed.post"


async def post(sess: Session, req: PostReq) -> Any:
    return await sess.record(req)
