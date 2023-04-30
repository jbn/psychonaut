from typing import Any, Optional, List
from pydantic import BaseModel, Field
from psychonaut.lexicon.formats import validate_at_uri, validate_cid, validate_datetime
from psychonaut.api.lexicons.app.bsky.actor.defs import ProfileViewBasic
from psychonaut.api.lexicons.app.bsky.embed.images import View
from psychonaut.api.lexicons.app.bsky.embed.record_with_media import View
from psychonaut.api.lexicons.com.atproto.label.defs import Label
from psychonaut.api.lexicons.app.bsky.embed.record import View
from psychonaut.api.lexicons.app.bsky.embed.external import View


class NotFoundPost(BaseModel):
    """
    [none provided by spec]
    """

    uri: str = Field(..., pre=True, validator=validate_at_uri)
    notFound: bool = Field(...)


class BlockedPost(BaseModel):
    """
    [none provided by spec]
    """

    uri: str = Field(..., pre=True, validator=validate_at_uri)
    blocked: bool = Field(...)


class ViewerState(BaseModel):
    """
    [none provided by spec]
    """

    repost: Optional[str] = Field(default=None, pre=True, validator=validate_at_uri)
    like: Optional[str] = Field(default=None, pre=True, validator=validate_at_uri)


class ReasonRepost(BaseModel):
    """
    [none provided by spec]
    """

    by: ProfileViewBasic
    indexedAt: str = Field(..., pre=True, validator=validate_datetime)


class PostView(BaseModel):
    """
    [none provided by spec]
    """

    uri: str = Field(..., pre=True, validator=validate_at_uri)
    cid: str = Field(..., pre=True, validator=validate_cid)
    author: ProfileViewBasic
    record: Any
    embed: Optional[Any] = None
    replyCount: Optional[int] = Field(default=None)
    repostCount: Optional[int] = Field(default=None)
    likeCount: Optional[int] = Field(default=None)
    indexedAt: str = Field(..., pre=True, validator=validate_datetime)
    viewer: Optional[ViewerState] = None
    labels: Optional[Any] = None


class ReplyRef(BaseModel):
    """
    [none provided by spec]
    """

    root: PostView
    parent: PostView


class ThreadViewPost(BaseModel):
    """
    [none provided by spec]
    """

    post: PostView
    parent: Optional[Any] = None
    replies: Optional[List[Any]] = Field(default=None)


class FeedViewPost(BaseModel):
    """
    [none provided by spec]
    """

    post: PostView
    reply: Optional[ReplyRef] = None
    reason: Optional[Any] = None
