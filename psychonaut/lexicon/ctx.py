from pathlib import Path
from pydantic import BaseModel, Field
from collections import OrderedDict, defaultdict
from typing import Dict, Optional, Set, Any
from psychonaut.lexicon.planner import LexiconDef


class GenCtx(BaseModel):
    imports: Dict[str, Set[str]] = Field(default_factory=lambda: defaultdict(set))
    fragments: OrderedDict[str, LexiconDef] = Field(default_factory=OrderedDict)
    verbose: bool = Field(default=False, repr=False)
    input_path: Optional[Path] = Field(default=None, repr=False)
    global_vars: Dict[str, Any] = Field(default_factory=dict, repr=False)

    def add_fragment(self, name: str, node: LexiconDef):
        assert name not in self.fragments, f"Fragment {name} already exists"
        self.fragments[name] = node

    @property
    def common_xrpc_id(self) -> Optional[str]:
        if not self.fragments:
            return None
        
        xrpc_ids = {
            v.node_id.split("#")[0]
            for v in self.fragments.values()
        }

        if len(xrpc_ids) == 1:
            return xrpc_ids.pop()

        raise ValueError(f"Multiple xrpc ids found: {xrpc_ids}")

    class Config:
        arbitrary_types_allowed = True