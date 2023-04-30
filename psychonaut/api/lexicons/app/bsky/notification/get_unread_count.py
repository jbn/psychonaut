from typing import Any, Optional
from psychonaut.api.session import Session
from pydantic import BaseModel, Field
from psychonaut.lexicon.formats import validate_datetime


class GetUnreadCountResp(BaseModel):
    count: int = Field(...)


class GetUnreadCountReq(BaseModel):
    """
    [none provided by spec]
    """

    seenAt: Optional[str] = Field(default=None, pre=True, validator=validate_datetime)

    @property
    def xrpc_id(self) -> str:
        return "app.bsky.notification.getUnreadCount"

    async def do_xrpc(self, sess: Session) -> GetUnreadCountResp:
        resp = await sess.query(self)
        return GetUnreadCountResp(**resp)
