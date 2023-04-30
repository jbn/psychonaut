from typing import Any, Optional
from psychonaut.api.lexicons.com.atproto.admin.defs import ReportView
from psychonaut.api.session import Session
from pydantic import BaseModel, Field


class GetModerationReportsResp(BaseModel):
    cursor: Optional[str] = Field(default=None)
    reports: Any


class GetModerationReportsReq(BaseModel):
    """
    List moderation reports related to a subject.
    """

    subject: Optional[str] = Field(default=None)
    resolved: Optional[bool] = Field(default=None)
    limit: Optional[int] = Field(default=50, ge=1, le=100)
    cursor: Optional[str] = Field(default=None)

    @property
    def xrpc_id(self) -> str:
        return "com.atproto.admin.getModerationReports"

    async def do_xrpc(self, sess: Session) -> GetModerationReportsResp:
        resp = await sess.query(self)
        return GetModerationReportsResp(**resp)
