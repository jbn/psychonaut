from typing import Any, Optional, List
from psychonaut.api.session import Session
from pydantic import BaseModel, Field
from psychonaut.lexicon.formats import validate_did


class ResolveModerationReportsReq(BaseModel):
    """
    Resolve moderation reports by an action.
    """

    actionId: int = Field(...)
    reportIds: List[int] = Field(...)
    createdBy: str = Field(..., pre=True, validator=validate_did)

    @property
    def xrpc_id(self) -> str:
        return "com.atproto.admin.resolveModerationReports"

    async def do_xrpc(self, sess: Session) -> Any:
        return await sess.procedure(self)
