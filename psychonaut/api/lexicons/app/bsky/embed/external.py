from typing import Any, Optional
from pydantic import BaseModel, Field
from psychonaut.lexicon.formats import validate_uri


class External(BaseModel):
    """
    [none provided by spec]
    """

    uri: str = Field(..., pre=True, validator=validate_uri)
    title: str = Field(...)
    description: str = Field(...)
    thumb: Optional[Any] = None


class ViewExternal(BaseModel):
    """
    [none provided by spec]
    """

    uri: str = Field(..., pre=True, validator=validate_uri)
    title: str = Field(...)
    description: str = Field(...)
    thumb: Optional[str] = Field(default=None)


class External(BaseModel):
    """
    [none provided by spec]
    """

    external: External


class View(BaseModel):
    """
    [none provided by spec]
    """

    external: ViewExternal
