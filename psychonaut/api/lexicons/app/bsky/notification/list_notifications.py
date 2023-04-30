from typing import Any, Optional
from psychonaut.api.lexicons.app.bsky.actor.defs import ProfileView
from psychonaut.api.lexicons.com.atproto.label.defs import Label
from pydantic import BaseModel, Field
from psychonaut.lexicon.formats import validate_at_uri, validate_cid, validate_datetime
from psychonaut.api.session import Session


class Notification(BaseModel):
    """
    [none provided by spec]
    """

    uri: str = Field(..., pre=True, validator=validate_at_uri)
    cid: str = Field(..., pre=True, validator=validate_cid)
    author: ProfileView
    reason: str = Field(
        ...,
        description="Expected values are 'like', 'repost', 'follow', 'mention', 'reply', and 'quote'.",
        known_values=["like", "repost", "follow", "mention", "reply", "quote"],
    )
    reasonSubject: Optional[str] = Field(
        default=None, pre=True, validator=validate_at_uri
    )
    record: Any
    isRead: bool = Field(...)
    indexedAt: str = Field(..., pre=True, validator=validate_datetime)
    labels: Optional[Any] = None


class ListNotificationsResp(BaseModel):
    cursor: Optional[str] = Field(default=None)
    notifications: Any


class ListNotificationsReq(BaseModel):
    """
    [none provided by spec]
    """

    limit: Optional[int] = Field(default=50, ge=1, le=100)
    cursor: Optional[str] = Field(default=None)
    seenAt: Optional[str] = Field(default=None, pre=True, validator=validate_datetime)

    @property
    def xrpc_id(self) -> str:
        return "app.bsky.notification.listNotifications"

    async def do_xrpc(self, sess: Session) -> ListNotificationsResp:
        resp = await sess.query(self)
        return ListNotificationsResp(**resp)
