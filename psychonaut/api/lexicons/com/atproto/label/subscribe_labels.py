from typing import Any, Optional
from pydantic import BaseModel, Field
from psychonaut.api.lexicons.com.atproto.label.defs import Label


class Info(BaseModel):
    """
    [none provided by spec]
    """

    name: str = Field(..., known_values=["OutdatedCursor"])
    message: Optional[str] = Field(default=None)


class Labels(BaseModel):
    """
    [none provided by spec]
    """

    seq: int = Field(...)
    labels: Any
