from pydantic import BaseModel, Field
from psychonaut.api.session import Session
from typing import Optional, Any


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


class GetModerationReportsResp(BaseModel):
    cursor: Optional[str] = Field(default=None)
    reports: Any

    @property
    def xrpc_id(self) -> str:
       return "com.atproto.admin.getModerationReports"


async def get_moderation_reports(sess: Session, req: GetModerationReportsReq) -> GetModerationReportsResp:
    resp = await sess.query(req)
    return GetModerationReportsResp(**resp)
