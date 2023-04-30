from typing import Any
from pydantic import BaseModel, Field
from psychonaut.lexicon.formats import validate_datetime
from psychonaut.api.session import Session


class AppPassword(BaseModel):
    """
    [none provided by spec]
    """

    name: str = Field(...)
    createdAt: str = Field(..., pre=True, validator=validate_datetime)


class ListAppPasswordsResp(BaseModel):
    passwords: Any


class ListAppPasswordsReq(BaseModel):
    """
    List all app-specific passwords.
    """

    @property
    def xrpc_id(self) -> str:
        return "com.atproto.server.listAppPasswords"

    async def do_xrpc(self, sess: Session) -> ListAppPasswordsResp:
        resp = await sess.query(self)
        return ListAppPasswordsResp(**resp)
