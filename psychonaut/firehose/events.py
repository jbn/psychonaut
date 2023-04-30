from enum import Enum
from dataclasses import Field
from typing import Optional, List, Union
from multiformats import CID
from pydantic import BaseModel

from psychonaut.lexicon.formats import validate_at_uri, validate_cid


# Event stream messages =====================================

class WriteOpAction(str, Enum):
    Create = "Create"
    Update = "Update"


class IndexRecord(BaseModel):
    type: str = "index_record"
    action: Union[WriteOpAction.Create, WriteOpAction.Update]
    # TODO: CID and URL make sense as types
    uri: str = Field(..., pre=True, validator=validate_at_uri)
    cid: CID = Field(..., pre=True, validator=validate_cid)
    obj: object
    timestamp: str


class DeleteRecord(BaseModel):
    type: str = "delete_record"
    uri: str = Field(..., pre=True, validator=validate_at_uri)
    cascading: bool


class DeleteRepo(BaseModel):
    type: str = "delete_repo"
    did: str


# Sequencer events =========================================
# /pds/src/sequencer/events.ts


# Replace this with the correct import for the schema
from placeholder import cid, bytes as schema_bytes

class ActionType(str, Enum):
    create = "create"
    update = "update"
    delete = "delete"

class CommitEvtOp(BaseModel):
    action: ActionType
    path: str
    cid: Optional[cid] = Field(default=None, pre=True, validator=validate_cid)

class CommitEvt(BaseModel):
    rebase: bool
    too_big: bool
    repo: str
    commit: cid = Field(..., pre=True, validator=validate_cid)
    prev: Optional[cid] = Field(default=None, pre=True, validator=validate_cid)
    blocks: bytes
    ops: List[CommitEvtOp]
    blobs: List[cid] = Field(default_factory=list, pre=True, validator=validate_cid)

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



