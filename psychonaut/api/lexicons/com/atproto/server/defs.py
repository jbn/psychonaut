from typing import Any
from pydantic import BaseModel, Field
from psychonaut.lexicon.formats import validate_did, validate_datetime


class InviteCodeUse(BaseModel):
    """
    [none provided by spec]
    """

    usedBy: str = Field(..., pre=True, validator=validate_did)
    usedAt: str = Field(..., pre=True, validator=validate_datetime)


class InviteCode(BaseModel):
    """
    [none provided by spec]
    """

    code: str = Field(...)
    available: int = Field(...)
    disabled: bool = Field(...)
    forAccount: str = Field(...)
    createdBy: str = Field(...)
    createdAt: str = Field(..., pre=True, validator=validate_datetime)
    uses: Any
