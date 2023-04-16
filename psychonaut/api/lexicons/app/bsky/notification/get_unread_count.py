from pydantic import BaseModel, Field
from psychonaut.lexicon.formats import validate_datetime
from psychonaut.api.session import Session
from typing import Optional, Any


class GetUnreadCountReq(BaseModel):
    seenAt: Optional[str] = Field(default=None, pre=True, validator=validate_datetime)

    @property
    def xrpc_id(self) -> str:
       return "app.bsky.notification.getUnreadCount"


class GetUnreadCountResp(BaseModel):
    count: int = Field(...)

    @property
    def xrpc_id(self) -> str:
       return "app.bsky.notification.getUnreadCount"


async def get_unread_count(sess: Session, req: GetUnreadCountReq) -> GetUnreadCountResp:
    resp = await sess.query(req)
    return GetUnreadCountResp(**resp)
