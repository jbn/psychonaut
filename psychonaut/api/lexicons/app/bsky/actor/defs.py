from typing import Any, Optional
from pydantic import BaseModel, Field
from psychonaut.lexicon.formats import (
    validate_at_uri,
    validate_handle,
    validate_did,
    validate_datetime,
)
from psychonaut.api.lexicons.com.atproto.label.defs import Label


class ViewerState(BaseModel):
    """
    [none provided by spec]
    """

    muted: Optional[bool] = Field(default=None)
    blockedBy: Optional[bool] = Field(default=None)
    blocking: Optional[str] = Field(default=None, pre=True, validator=validate_at_uri)
    following: Optional[str] = Field(default=None, pre=True, validator=validate_at_uri)
    followedBy: Optional[str] = Field(default=None, pre=True, validator=validate_at_uri)


class ProfileViewBasic(BaseModel):
    """
    [none provided by spec]
    """

    did: str = Field(..., pre=True, validator=validate_did)
    handle: str = Field(..., pre=True, validator=validate_handle)
    displayName: Optional[str] = Field(default=None, max_length=640)
    avatar: Optional[str] = Field(default=None)
    viewer: Optional[ViewerState] = None
    labels: Optional[Any] = None


class ProfileView(BaseModel):
    """
    [none provided by spec]
    """

    did: str = Field(..., pre=True, validator=validate_did)
    handle: str = Field(..., pre=True, validator=validate_handle)
    displayName: Optional[str] = Field(default=None, max_length=640)
    description: Optional[str] = Field(default=None, max_length=2560)
    avatar: Optional[str] = Field(default=None)
    indexedAt: Optional[str] = Field(
        default=None, pre=True, validator=validate_datetime
    )
    viewer: Optional[ViewerState] = None
    labels: Optional[Any] = None


class ProfileViewDetailed(BaseModel):
    """
    [none provided by spec]
    """

    did: str = Field(..., pre=True, validator=validate_did)
    handle: str = Field(..., pre=True, validator=validate_handle)
    displayName: Optional[str] = Field(default=None, max_length=640)
    description: Optional[str] = Field(default=None, max_length=2560)
    avatar: Optional[str] = Field(default=None)
    banner: Optional[str] = Field(default=None)
    followersCount: Optional[int] = Field(default=None)
    followsCount: Optional[int] = Field(default=None)
    postsCount: Optional[int] = Field(default=None)
    indexedAt: Optional[str] = Field(
        default=None, pre=True, validator=validate_datetime
    )
    viewer: Optional[ViewerState] = None
    labels: Optional[Any] = None
