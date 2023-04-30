from typing import Any, Optional, List
from psychonaut.api.lexicons.app.bsky.actor.defs import ProfileViewDetailed
from psychonaut.api.session import Session
from pydantic import BaseModel, Field
from psychonaut.lexicon.formats import validate_at_identifier, validate_array


class GetProfilesResp(BaseModel):
    profiles: Any


class GetProfilesReq(BaseModel):
    """
    [none provided by spec]
    """

    actors: List[str] = Field(
        ..., max_items=25, pre=True, validator=validate_array(validate_at_identifier)
    )

    @property
    def xrpc_id(self) -> str:
        return "app.bsky.actor.getProfiles"

    async def do_xrpc(self, sess: Session) -> GetProfilesResp:
        resp = await sess.query(self)
        return GetProfilesResp(**resp)
