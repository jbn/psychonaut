from typing import Any
from pydantic import BaseModel, Field


class Image(BaseModel):
    """
    [none provided by spec]
    """

    image: Any
    alt: str = Field(...)


class ViewImage(BaseModel):
    """
    [none provided by spec]
    """

    thumb: str = Field(...)
    fullsize: str = Field(...)
    alt: str = Field(...)


class Images(BaseModel):
    """
    [none provided by spec]
    """

    images: Any


class View(BaseModel):
    """
    [none provided by spec]
    """

    images: Any
