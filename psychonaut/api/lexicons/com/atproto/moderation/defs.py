from typing import Any
from enum import auto, Enum


class ReasonType(str, Enum):
    REASONVIOLATION = "reasonViolation"
    REASONOTHER = "reasonOther"
    REASONSPAM = "reasonSpam"
    REASONMISLEADING = "reasonMisleading"
    REASONRUDE = "reasonRude"
    REASONSEXUAL = "reasonSexual"
