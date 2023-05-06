# See snarfed's code:
#
# https://github.com/snarfed/bridgy-fed/blob/main/atproto_mst.py

from argparse import OPTIONAL
from typing import List
from multiformats import CID
from pydantic import BaseModel


class Entry(BaseModel):
    p: int  # prefix length
    k: str  # remainder of key
    v: CID  # value
    t: OPTIONAL[CID]  # next subtree


class Data(BaseModel):
    e: List[Entry]  # entries
    l: OPTIONAL[CID]  # left-most subtree


class Leaf(BaseModel):
    key: str
    value: CID


class MST:
    