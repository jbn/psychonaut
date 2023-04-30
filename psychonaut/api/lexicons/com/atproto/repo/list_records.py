from typing import Any, Optional
from pydantic import BaseModel, Field
from psychonaut.lexicon.formats import (
    validate_at_uri,
    validate_cid,
    validate_at_identifier,
    validate_nsid,
)
from psychonaut.api.session import Session


class Record(BaseModel):
    """
    [none provided by spec]
    """

    uri: str = Field(..., pre=True, validator=validate_at_uri)
    cid: str = Field(..., pre=True, validator=validate_cid)
    value: Any


class ListRecordsResp(BaseModel):
    cursor: Optional[str] = Field(default=None)
    records: Any


class ListRecordsReq(BaseModel):
    """
    List a range of records in a collection.
    """

    repo: str = Field(
        ...,
        description="The handle or DID of the repo.",
        pre=True,
        validator=validate_at_identifier,
    )
    collection: str = Field(
        ...,
        description="The NSID of the record type.",
        pre=True,
        validator=validate_nsid,
    )
    limit: Optional[int] = Field(
        default=50, description="The number of records to return.", ge=1, le=100
    )
    cursor: Optional[str] = Field(default=None)
    rkeyStart: Optional[str] = Field(
        default=None,
        description="DEPRECATED: The lowest sort-ordered rkey to start from (exclusive)",
    )
    rkeyEnd: Optional[str] = Field(
        default=None,
        description="DEPRECATED: The highest sort-ordered rkey to stop at (exclusive)",
    )
    reverse: Optional[bool] = Field(
        default=None, description="Reverse the order of the returned records?"
    )

    @property
    def xrpc_id(self) -> str:
        return "com.atproto.repo.listRecords"

    async def do_xrpc(self, sess: Session) -> ListRecordsResp:
        resp = await sess.query(self)
        return ListRecordsResp(**resp)
