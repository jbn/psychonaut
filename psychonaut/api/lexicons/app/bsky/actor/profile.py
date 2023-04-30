from typing import Any, Optional
from pydantic import BaseModel, Field


class Profile(BaseModel):
    """
    [none provided by spec]
    """

    displayName: Optional[str] = Field(default=None, max_length=640)
    description: Optional[str] = Field(default=None, max_length=2560)
    avatar: Optional[Any] = None
    banner: Optional[Any] = None

    @property
    def xrpc_id(self) -> str:
        return "app.bsky.actor.profile"
