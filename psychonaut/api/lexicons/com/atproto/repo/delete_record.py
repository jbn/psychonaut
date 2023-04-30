from typing import Any, Optional
from psychonaut.api.session import Session
from pydantic import BaseModel, Field
from psychonaut.lexicon.formats import (
    validate_cid,
    validate_at_identifier,
    validate_nsid,
)


class DeleteRecordReq(BaseModel):
    """
    Delete a record, or ensure it doesn't exist.
    """

    repo: str = Field(
        ...,
        description="The handle or DID of the repo.",
        pre=True,
        validator=validate_at_identifier,
    )
    collection: str = Field(
        ...,
        description="The NSID of the record collection.",
        pre=True,
        validator=validate_nsid,
    )
    rkey: str = Field(..., description="The key of the record.")
    swapRecord: Optional[str] = Field(
        default=None,
        description="Compare and swap with the previous record by cid.",
        pre=True,
        validator=validate_cid,
    )
    swapCommit: Optional[str] = Field(
        default=None,
        description="Compare and swap with the previous commit by cid.",
        pre=True,
        validator=validate_cid,
    )

    @property
    def xrpc_id(self) -> str:
        return "com.atproto.repo.deleteRecord"

    async def do_xrpc(self, sess: Session) -> Any:
        return await sess.procedure(self)
