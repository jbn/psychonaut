from typing import Any, Optional
from psychonaut.api.session import Session
from pydantic import BaseModel, Field
from psychonaut.lexicon.formats import validate_cid, validate_did


class GetRepoReq(BaseModel):
    """
    Gets the repo state.
    """

    did: str = Field(
        ..., description="The DID of the repo.", pre=True, validator=validate_did
    )
    earliest: Optional[str] = Field(
        default=None,
        description="The earliest commit in the commit range (not inclusive)",
        pre=True,
        validator=validate_cid,
    )
    latest: Optional[str] = Field(
        default=None,
        description="The latest commit in the commit range (inclusive)",
        pre=True,
        validator=validate_cid,
    )

    @property
    def xrpc_id(self) -> str:
        return "com.atproto.sync.getRepo"

    async def do_xrpc(self, sess: Session) -> Any:
        return await sess.query(self)
