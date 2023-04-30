from typing import Any, Optional, List
from pydantic import BaseModel, Field
from psychonaut.lexicon.formats import (
    validate_cid,
    validate_did,
    validate_datetime,
    validate_array,
    validate_at_uri,
    validate_handle,
)
from enum import auto, Enum
from psychonaut.api.lexicons.com.atproto.moderation.defs import ReasonType
from psychonaut.api.lexicons.com.atproto.server.defs import InviteCode
from psychonaut.api.lexicons.com.atproto.label.defs import Label


class RepoRef(BaseModel):
    """
    [none provided by spec]
    """

    did: str = Field(..., pre=True, validator=validate_did)


class ActionReversal(BaseModel):
    """
    [none provided by spec]
    """

    reason: str = Field(...)
    createdBy: str = Field(..., pre=True, validator=validate_did)
    createdAt: str = Field(..., pre=True, validator=validate_datetime)


class VideoDetails(BaseModel):
    """
    [none provided by spec]
    """

    width: int = Field(...)
    height: int = Field(...)
    length: int = Field(...)


class ImageDetails(BaseModel):
    """
    [none provided by spec]
    """

    width: int = Field(...)
    height: int = Field(...)


class ActionType(str, Enum):
    TAKEDOWN = "takedown"
    FLAG = "flag"
    ACKNOWLEDGE = "acknowledge"


class ActionView(BaseModel):
    """
    [none provided by spec]
    """

    id: int = Field(...)
    action: ActionType
    subject: Any
    subjectBlobCids: List[str] = Field(...)
    createLabelVals: Optional[List[str]] = Field(default=None)
    negateLabelVals: Optional[List[str]] = Field(default=None)
    reason: str = Field(...)
    createdBy: str = Field(..., pre=True, validator=validate_did)
    createdAt: str = Field(..., pre=True, validator=validate_datetime)
    reversal: Optional[ActionReversal] = None
    resolvedReportIds: List[int] = Field(...)


class ActionViewCurrent(BaseModel):
    """
    [none provided by spec]
    """

    id: int = Field(...)
    action: ActionType


class ReportView(BaseModel):
    """
    [none provided by spec]
    """

    id: int = Field(...)
    reasonType: ReasonType
    reason: Optional[str] = Field(default=None)
    subject: Any
    reportedBy: str = Field(..., pre=True, validator=validate_did)
    createdAt: str = Field(..., pre=True, validator=validate_datetime)
    resolvedByActionIds: List[int] = Field(...)


class Moderation(BaseModel):
    """
    [none provided by spec]
    """

    currentAction: Optional[ActionViewCurrent] = None


class ModerationDetail(BaseModel):
    """
    [none provided by spec]
    """

    currentAction: Optional[ActionViewCurrent] = None
    actions: Any
    reports: Any


class RepoView(BaseModel):
    """
    [none provided by spec]
    """

    did: str = Field(..., pre=True, validator=validate_did)
    handle: str = Field(..., pre=True, validator=validate_handle)
    email: Optional[str] = Field(default=None)
    relatedRecords: List[Any] = Field(...)
    indexedAt: str = Field(..., pre=True, validator=validate_datetime)
    moderation: Moderation
    invitedBy: Optional[InviteCode] = None


class BlobView(BaseModel):
    """
    [none provided by spec]
    """

    cid: str = Field(..., pre=True, validator=validate_cid)
    mimeType: str = Field(...)
    size: int = Field(...)
    createdAt: str = Field(..., pre=True, validator=validate_datetime)
    details: Optional[Any] = None
    moderation: Optional[Moderation] = None


class RepoViewDetail(BaseModel):
    """
    [none provided by spec]
    """

    did: str = Field(..., pre=True, validator=validate_did)
    handle: str = Field(..., pre=True, validator=validate_handle)
    email: Optional[str] = Field(default=None)
    relatedRecords: List[Any] = Field(...)
    indexedAt: str = Field(..., pre=True, validator=validate_datetime)
    moderation: ModerationDetail
    labels: Optional[Any] = None
    invitedBy: Optional[InviteCode] = None
    invites: Optional[Any] = None


class RecordView(BaseModel):
    """
    [none provided by spec]
    """

    uri: str = Field(..., pre=True, validator=validate_at_uri)
    cid: str = Field(..., pre=True, validator=validate_cid)
    value: Any
    blobCids: List[str] = Field(..., pre=True, validator=validate_array(validate_cid))
    indexedAt: str = Field(..., pre=True, validator=validate_datetime)
    moderation: Moderation
    repo: RepoView


class RecordViewDetail(BaseModel):
    """
    [none provided by spec]
    """

    uri: str = Field(..., pre=True, validator=validate_at_uri)
    cid: str = Field(..., pre=True, validator=validate_cid)
    value: Any
    blobs: Any
    labels: Optional[Any] = None
    indexedAt: str = Field(..., pre=True, validator=validate_datetime)
    moderation: ModerationDetail
    repo: RepoView


class ActionViewDetail(BaseModel):
    """
    [none provided by spec]
    """

    id: int = Field(...)
    action: ActionType
    subject: Any
    subjectBlobs: Any
    createLabelVals: Optional[List[str]] = Field(default=None)
    negateLabelVals: Optional[List[str]] = Field(default=None)
    reason: str = Field(...)
    createdBy: str = Field(..., pre=True, validator=validate_did)
    createdAt: str = Field(..., pre=True, validator=validate_datetime)
    reversal: Optional[ActionReversal] = None
    resolvedReports: Any


class ReportViewDetail(BaseModel):
    """
    [none provided by spec]
    """

    id: int = Field(...)
    reasonType: ReasonType
    reason: Optional[str] = Field(default=None)
    subject: Any
    reportedBy: str = Field(..., pre=True, validator=validate_did)
    createdAt: str = Field(..., pre=True, validator=validate_datetime)
    resolvedByActions: Any
