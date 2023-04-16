from pydantic import BaseModel, Field
from psychonaut.api.session import Session
from typing import Optional, Any


class ListAppPasswordsReq(BaseModel):
    """
    List all app-specific passwords.
    """

    @property
    def xrpc_id(self) -> str:
       return "com.atproto.server.listAppPasswords"


class ListAppPasswordsResp(BaseModel):
    passwords: Any

    @property
    def xrpc_id(self) -> str:
       return "com.atproto.server.listAppPasswords"


async def list_app_passwords(sess: Session, req: ListAppPasswordsReq) -> ListAppPasswordsResp:
    resp = await sess.query(req)
    return ListAppPasswordsResp(**resp)
