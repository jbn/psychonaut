from typing import Any, Optional
from psychonaut.api.session import Session
from pydantic import BaseModel, Field
from psychonaut.lexicon.formats import validate_at_uri, validate_cid


class GetRecordReq(BaseModel):
    """
    View details about a record.
    """

    uri: str = Field(..., pre=True, validator=validate_at_uri)
    cid: Optional[str] = Field(default=None, pre=True, validator=validate_cid)

    @property
    def xrpc_id(self) -> str:
        return "com.atproto.admin.getRecord"

    async def do_xrpc(self, sess: Session) -> Any:
        return await sess.query(self)
