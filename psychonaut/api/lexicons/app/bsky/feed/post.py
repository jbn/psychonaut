from typing import Any, Optional
from pydantic import BaseModel, Field
from psychonaut.api.lexicons.com.atproto.repo.strong_ref import StrongRef
from psychonaut.lexicon.formats import validate_datetime


class TextSlice(BaseModel):
    """
    Deprecated. Use app.bsky.richtext instead -- A text segment. Start is
    inclusive, end is exclusive. Indices are for utf16-encoded strings.
    """

    start: int = Field(..., ge=0)
    end: int = Field(..., ge=0)


class ReplyRef(BaseModel):
    """
    [none provided by spec]
    """

    root: StrongRef
    parent: StrongRef


class Entity(BaseModel):
    """
    Deprecated: use facets instead.
    """

    index: TextSlice
    type: str = Field(..., description="Expected values are 'mention' and 'link'.")
    value: str = Field(...)


class Post(BaseModel):
    """
    [none provided by spec]
    """

    text: str = Field(..., max_length=3000)
    entities: Optional[Any] = None
    facets: Optional[Any] = None
    reply: Optional[ReplyRef] = None
    embed: Optional[Any] = None
    createdAt: str = Field(..., pre=True, validator=validate_datetime)

    @property
    def xrpc_id(self) -> str:
        return "app.bsky.feed.post"
