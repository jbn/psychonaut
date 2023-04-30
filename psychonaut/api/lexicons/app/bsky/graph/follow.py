from typing import Any
from pydantic import BaseModel, Field
from psychonaut.lexicon.formats import validate_did, validate_datetime


class Follow(BaseModel):
    """
    A social follow.
    """

    subject: str = Field(..., pre=True, validator=validate_did)
    createdAt: str = Field(..., pre=True, validator=validate_datetime)

    @property
    def xrpc_id(self) -> str:
        return "app.bsky.graph.follow"
