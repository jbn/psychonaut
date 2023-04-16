from pydantic import BaseModel, Field
from typing import Optional, List, Any
from psychonaut.lexicon.formats import validate_array, validate_at_identifier
from psychonaut.api.session import Session


class GetProfilesReq(BaseModel):
    actors: List[str] = Field(..., max_items=25, pre=True, validator=validate_array(validate_at_identifier))

    @property
    def xrpc_id(self) -> str:
       return "app.bsky.actor.getProfiles"


class GetProfilesResp(BaseModel):
    profiles: Any

    @property
    def xrpc_id(self) -> str:
       return "app.bsky.actor.getProfiles"


async def get_profiles(sess: Session, req: GetProfilesReq) -> GetProfilesResp:
    resp = await sess.query(req)
    return GetProfilesResp(**resp)
