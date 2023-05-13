from enum import Enum
from typing import Optional, List, Union
from multiformats import CID
from pydantic import BaseModel, Field

from psychonaut.lexicon.formats import validate_at_uri, validate_cid


# Event stream messages =====================================


class WriteOpAction(str, Enum):
    Create = "Create"
    Update = "Update"


# TODO: CID and URL ddmake sense as types
class IndexRecord(BaseModel):
    type: str = "index_record"
    action: str = Field(..., pre=True, validator=WriteOpAction.__contains__)
    uri: str = Field(..., pre=True, validator=validate_at_uri)
    cid: CID = Field(..., pre=True, validator=validate_cid)
    obj: object
    timestamp: str

    class Config:
        json_encoders = { CID: str }
        arbitrary_types_allowed = True



class DeleteRecord(BaseModel):
    type: str = "delete_record"
    uri: str = Field(..., pre=True, validator=validate_at_uri)
    cascading: bool


class DeleteRepo(BaseModel):
    type: str = "delete_repo"
    did: str


# Sequencer events =========================================
# /pds/src/sequencer/events.ts


class ActionType(str, Enum):
    create = "create"
    update = "update"
    delete = "delete"


class CommitEvtOp(BaseModel):
    action: ActionType
    path: str
    cid: Optional[CID] = Field(default=None, pre=True, validator=validate_cid)

    class Config:
        json_encoders = { CID: str }
        arbitrary_types_allowed = True


class CommitEvt(BaseModel):
    repo: str
    ops: List[CommitEvtOp]
    commit: CID = Field(..., pre=True, validator=validate_cid)
    prev: Optional[CID] = Field(default=None, pre=True, validator=validate_cid)
    blocks: bytes
    blobs: List[CID] = Field(default_factory=list, pre=True, validator=validate_cid)
    rebase: bool
    too_big: bool = Field(..., alias="tooBig")

    class Config:
        json_encoders = { CID: str }
        arbitrary_types_allowed = True


class HandleEvt(BaseModel):
    did: str
    handle: str


class TypedCommitEvt(BaseModel):
    type: str = Field("commit", const=True)
    seq: int
    time: str
    evt: CommitEvt


class TypedHandleEvt(BaseModel):
    type: str = Field("handle", const=True)
    seq: int
    time: str
    evt: HandleEvt


SeqEvt = Union[TypedCommitEvt, TypedHandleEvt]
