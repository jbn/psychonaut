from typing import Any, Optional
from psychonaut.api.lexicons.com.atproto.moderation.defs import ReasonType
from psychonaut.api.lexicons.com.atproto.admin.defs import RepoRef
from psychonaut.api.session import Session
from pydantic import BaseModel, Field
from psychonaut.lexicon.formats import validate_did, validate_datetime


class CreateReportResp(BaseModel):
    id: int = Field(...)
    reasonType: ReasonType
    reason: Optional[str] = Field(default=None)
    subject: Any
    reportedBy: str = Field(..., pre=True, validator=validate_did)
    createdAt: str = Field(..., pre=True, validator=validate_datetime)


class CreateReportReq(BaseModel):
    """
    Report a repo or a record.
    """

    reasonType: ReasonType
    reason: Optional[str] = Field(default=None)
    subject: Any

    @property
    def xrpc_id(self) -> str:
        return "com.atproto.moderation.createReport"

    async def do_xrpc(self, sess: Session) -> CreateReportResp:
        resp = await sess.procedure(self)
        return CreateReportResp(**resp)
