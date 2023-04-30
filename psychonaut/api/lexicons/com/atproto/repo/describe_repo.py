from typing import Any, Optional, List
from psychonaut.api.session import Session
from pydantic import BaseModel, Field
from psychonaut.lexicon.formats import (
    validate_at_identifier,
    validate_handle,
    validate_array,
    validate_did,
    validate_nsid,
)


class DescribeRepoResp(BaseModel):
    handle: str = Field(..., pre=True, validator=validate_handle)
    did: str = Field(..., pre=True, validator=validate_did)
    didDoc: Any
    collections: List[str] = Field(
        ..., pre=True, validator=validate_array(validate_nsid)
    )
    handleIsCorrect: bool = Field(...)


class DescribeRepoReq(BaseModel):
    """
    Get information about the repo, including the list of collections.
    """

    repo: str = Field(
        ...,
        description="The handle or DID of the repo.",
        pre=True,
        validator=validate_at_identifier,
    )

    @property
    def xrpc_id(self) -> str:
        return "com.atproto.repo.describeRepo"

    async def do_xrpc(self, sess: Session) -> DescribeRepoResp:
        resp = await sess.query(self)
        return DescribeRepoResp(**resp)
