from typing import Any
from psychonaut.api.session import Session
from pydantic import BaseModel, Field
from psychonaut.lexicon.formats import validate_at_identifier


class UpdateAccountEmailReq(BaseModel):
    """
    Administrative action to update an account's email
    """

    account: str = Field(
        ...,
        description="The handle or DID of the repo.",
        pre=True,
        validator=validate_at_identifier,
    )
    email: str = Field(...)

    @property
    def xrpc_id(self) -> str:
        return "com.atproto.admin.updateAccountEmail"

    async def do_xrpc(self, sess: Session) -> Any:
        return await sess.procedure(self)
