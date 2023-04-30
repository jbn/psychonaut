from typing import Any, Optional
from psychonaut.api.session import Session
from pydantic import BaseModel, Field
from psychonaut.lexicon.formats import validate_cid, validate_did, validate_nsid


class GetRecordReq(BaseModel):
    """
    Gets blocks needed for existence or non-existence of record.
    """

    did: str = Field(
        ..., description="The DID of the repo.", pre=True, validator=validate_did
    )
    collection: str = Field(..., pre=True, validator=validate_nsid)
    rkey: str = Field(...)
    commit: Optional[str] = Field(
        default=None,
        description="An optional past commit CID.",
        pre=True,
        validator=validate_cid,
    )

    @property
    def xrpc_id(self) -> str:
        return "com.atproto.sync.getRecord"

    async def do_xrpc(self, sess: Session) -> Any:
        return await sess.query(self)
