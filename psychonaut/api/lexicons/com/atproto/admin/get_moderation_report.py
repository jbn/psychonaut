from pydantic import BaseModel, Field
from psychonaut.api.session import Session
from typing import Optional, Any


class GetModerationReportReq(BaseModel):
    """
    View details about a moderation report.
    """
    id: int = Field(...)

    @property
    def xrpc_id(self) -> str:
       return "com.atproto.admin.getModerationReport"


async def get_moderation_report(sess: Session, req: GetModerationReportReq) -> Any:
    return await sess.query(req)
