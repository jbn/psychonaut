from typing import Any
from pydantic import BaseModel, Field
from psychonaut.lexicon.formats import validate_at_uri, validate_cid


class StrongRef(BaseModel):
    """
    [none provided by spec]
    """

    uri: str = Field(..., pre=True, validator=validate_at_uri)
    cid: str = Field(..., pre=True, validator=validate_cid)
