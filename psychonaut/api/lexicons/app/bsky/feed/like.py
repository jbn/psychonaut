from typing import Any
from pydantic import BaseModel, Field
from psychonaut.api.lexicons.com.atproto.repo.strong_ref import StrongRef
from psychonaut.lexicon.formats import validate_datetime


class Like(BaseModel):
    """
    [none provided by spec]
    """

    subject: StrongRef
    createdAt: str = Field(..., pre=True, validator=validate_datetime)

    @property
    def xrpc_id(self) -> str:
        return "app.bsky.feed.like"
