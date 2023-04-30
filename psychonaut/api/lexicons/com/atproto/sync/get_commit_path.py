from typing import Any, Optional, List
from psychonaut.api.session import Session
from pydantic import BaseModel, Field
from psychonaut.lexicon.formats import validate_cid, validate_did, validate_array


class GetCommitPathResp(BaseModel):
    commits: List[str] = Field(..., pre=True, validator=validate_array(validate_cid))


class GetCommitPathReq(BaseModel):
    """
    Gets the path of repo commits
    """

    did: str = Field(
        ..., description="The DID of the repo.", pre=True, validator=validate_did
    )
    latest: Optional[str] = Field(
        default=None,
        description="The most recent commit",
        pre=True,
        validator=validate_cid,
    )
    earliest: Optional[str] = Field(
        default=None,
        description="The earliest commit to start from",
        pre=True,
        validator=validate_cid,
    )

    @property
    def xrpc_id(self) -> str:
        return "com.atproto.sync.getCommitPath"

    async def do_xrpc(self, sess: Session) -> GetCommitPathResp:
        resp = await sess.query(self)
        return GetCommitPathResp(**resp)
