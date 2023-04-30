from typing import Any, Optional, List
from pydantic import BaseModel, Field
from psychonaut.lexicon.formats import (
    validate_cid,
    validate_at_identifier,
    validate_nsid,
)
from psychonaut.api.session import Session


class Delete(BaseModel):
    """
    Delete an existing record.
    """

    collection: str = Field(..., pre=True, validator=validate_nsid)
    rkey: str = Field(...)


class Create(BaseModel):
    """
    Create a new record.
    """

    collection: str = Field(..., pre=True, validator=validate_nsid)
    rkey: Optional[str] = Field(default=None)
    value: Any


class Update(BaseModel):
    """
    Update an existing record.
    """

    collection: str = Field(..., pre=True, validator=validate_nsid)
    rkey: str = Field(...)
    value: Any


class ApplyWritesReq(BaseModel):
    """
    Apply a batch transaction of creates, updates, and deletes.
    """

    repo: str = Field(
        ...,
        description="The handle or DID of the repo.",
        pre=True,
        validator=validate_at_identifier,
    )
    validate_flag: Optional[bool] = Field(
        alias="validate", default=True, description="Validate the records?"
    )
    writes: List[Any] = Field(...)
    swapCommit: Optional[str] = Field(default=None, pre=True, validator=validate_cid)

    @property
    def xrpc_id(self) -> str:
        return "com.atproto.repo.applyWrites"

    async def do_xrpc(self, sess: Session) -> Any:
        return await sess.procedure(self)
