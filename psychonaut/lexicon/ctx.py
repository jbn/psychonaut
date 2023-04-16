from pydantic import BaseModel, Field
from collections import defaultdict
from typing import Dict, Set


class GenCtx(BaseModel):
    imports: Dict[str, Set[str]] = Field(default_factory=lambda: defaultdict(set))