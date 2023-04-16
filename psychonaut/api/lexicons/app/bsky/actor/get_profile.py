from pydantic import BaseModel, Field
from psychonaut.lexicon.formats import validate_at_identifier
from psychonaut.api.session import Session
from typing import Optional, Any


class GetProfileReq(BaseModel):
    actor: str = Field(..., pre=True, validator=validate_at_identifier)

    @property
    def xrpc_id(self) -> str:
       return "app.bsky.actor.getProfile"


async def get_profile(sess: Session, req: GetProfileReq) -> Any:
    return await sess.query(req)
