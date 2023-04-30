from typing import Any, Optional, List
from pydantic import BaseModel, Field
from psychonaut.lexicon.formats import validate_handle, validate_did, validate_datetime


class Handle(BaseModel):
    """
    [none provided by spec]
    """

    seq: int = Field(...)
    did: str = Field(..., pre=True, validator=validate_did)
    handle: str = Field(..., pre=True, validator=validate_handle)
    time: str = Field(..., pre=True, validator=validate_datetime)


class Tombstone(BaseModel):
    """
    [none provided by spec]
    """

    seq: int = Field(...)
    did: str = Field(..., pre=True, validator=validate_did)
    time: str = Field(..., pre=True, validator=validate_datetime)


class Migrate(BaseModel):
    """
    [none provided by spec]
    """

    seq: int = Field(...)
    did: str = Field(..., pre=True, validator=validate_did)
    migrateTo: str = Field(...)
    time: str = Field(..., pre=True, validator=validate_datetime)


class Info(BaseModel):
    """
    [none provided by spec]
    """

    name: str = Field(..., known_values=["OutdatedCursor"])
    message: Optional[str] = Field(default=None)


class RepoOp(BaseModel):
    """
    [none provided by spec]
    """

    action: str = Field(..., known_values=["create", "update", "delete"])
    path: str = Field(...)
    cid: Any


class Commit(BaseModel):
    """
    [none provided by spec]
    """

    seq: int = Field(...)
    rebase: bool = Field(...)
    tooBig: bool = Field(...)
    repo: str = Field(..., pre=True, validator=validate_did)
    commit: Any
    prev: Any
    blocks: Any
    ops: Any
    blobs: List[Any] = Field(...)
    time: str = Field(..., pre=True, validator=validate_datetime)
