from typing import Any
from psychonaut.api.session import Session
from pydantic import BaseModel, Field
from psychonaut.lexicon.formats import validate_datetime


class CreateAppPasswordReq(BaseModel):
    """
    Create an app-specific password.
    """

    name: str = Field(...)

    @property
    def xrpc_id(self) -> str:
        return "com.atproto.server.createAppPassword"

    async def do_xrpc(self, sess: Session) -> Any:
        return await sess.procedure(self)


class AppPassword(BaseModel):
    """
    [none provided by spec]
    """

    name: str = Field(...)
    password: str = Field(...)
    createdAt: str = Field(..., pre=True, validator=validate_datetime)
