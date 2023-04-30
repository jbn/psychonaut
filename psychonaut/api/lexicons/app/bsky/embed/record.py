from typing import Any, Optional, List
from pydantic import BaseModel, Field
from psychonaut.lexicon.formats import validate_at_uri, validate_cid, validate_datetime
from psychonaut.api.lexicons.app.bsky.actor.defs import ProfileViewBasic
from psychonaut.api.lexicons.com.atproto.repo.strong_ref import StrongRef


class ViewBlocked(BaseModel):
    """
    [none provided by spec]
    """

    uri: str = Field(..., pre=True, validator=validate_at_uri)


class ViewNotFound(BaseModel):
    """
    [none provided by spec]
    """

    uri: str = Field(..., pre=True, validator=validate_at_uri)


class ViewRecord(BaseModel):
    """
    [none provided by spec]
    """

    uri: str = Field(..., pre=True, validator=validate_at_uri)
    cid: str = Field(..., pre=True, validator=validate_cid)
    author: ProfileViewBasic
    value: Any
    labels: Optional[Any] = None
    embeds: Optional[List[Any]] = Field(default=None)
    indexedAt: str = Field(..., pre=True, validator=validate_datetime)


class Record(BaseModel):
    """
    [none provided by spec]
    """

    record: StrongRef


class View(BaseModel):
    """
    [none provided by spec]
    """

    record: Any
