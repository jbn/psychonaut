from typing import Any
from pydantic import BaseModel, Field
from psychonaut.api.lexicons.app.bsky.embed.record import View, Record
from psychonaut.api.lexicons.app.bsky.embed.images import View
from psychonaut.api.lexicons.app.bsky.embed.external import View


class RecordWithMedia(BaseModel):
    """
    [none provided by spec]
    """

    record: Record
    media: Any


class View(BaseModel):
    """
    [none provided by spec]
    """

    record: View
    media: Any
