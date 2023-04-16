from pydantic import BaseModel, Field
from psychonaut.lexicon.formats import validate_datetime
from psychonaut.api.session import Session
from typing import Optional, Any


class ListNotificationsReq(BaseModel):
    limit: Optional[int] = Field(default=50, ge=1, le=100)
    cursor: Optional[str] = Field(default=None)
    seenAt: Optional[str] = Field(default=None, pre=True, validator=validate_datetime)

    @property
    def xrpc_id(self) -> str:
       return "app.bsky.notification.listNotifications"


class ListNotificationsResp(BaseModel):
    cursor: Optional[str] = Field(default=None)
    notifications: Any

    @property
    def xrpc_id(self) -> str:
       return "app.bsky.notification.listNotifications"


async def list_notifications(sess: Session, req: ListNotificationsReq) -> ListNotificationsResp:
    resp = await sess.query(req)
    return ListNotificationsResp(**resp)
