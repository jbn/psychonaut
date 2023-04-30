from typing import Any
from psychonaut.api.session import Session
from pydantic import BaseModel, Field


class GetModerationReportReq(BaseModel):
    """
    View details about a moderation report.
    """

    id: int = Field(...)

    @property
    def xrpc_id(self) -> str:
        return "com.atproto.admin.getModerationReport"

    async def do_xrpc(self, sess: Session) -> Any:
        return await sess.query(self)
