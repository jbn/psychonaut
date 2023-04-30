from typing import Any, Optional, List
from psychonaut.api.lexicons.com.atproto.admin.defs import RepoRef
from psychonaut.api.session import Session
from pydantic import BaseModel, Field
from psychonaut.lexicon.formats import validate_cid, validate_did, validate_array


class TakeModerationActionReq(BaseModel):
    """
    Take a moderation action on a repo.
    """

    action: str = Field(
        ...,
        known_values=[
            "com.atproto.admin.defs#takedown",
            "com.atproto.admin.defs#flag",
            "com.atproto.admin.defs#acknowledge",
        ],
    )
    subject: Any
    subjectBlobCids: Optional[List[str]] = Field(
        default=None, pre=True, validator=validate_array(validate_cid)
    )
    createLabelVals: Optional[List[str]] = Field(default=None)
    negateLabelVals: Optional[List[str]] = Field(default=None)
    reason: str = Field(...)
    createdBy: str = Field(..., pre=True, validator=validate_did)

    @property
    def xrpc_id(self) -> str:
        return "com.atproto.admin.takeModerationAction"

    async def do_xrpc(self, sess: Session) -> Any:
        return await sess.procedure(self)
