"""
See: https://github.com/bluesky-social/atproto/blob/main/packages/lexicon/src/blob-refs.ts
"""
from __future__ import annotations
from typing import Any, Dict, Optional, Union
from pydantic import BaseModel, Field, validator
from multiformats.cid import CID
from psychonaut.common_web.ipld import ipld_to_json


# TODO: test

class TypedJsonBlobRef(BaseModel):
    type_kludge: str = Field(..., alias='$type', const='blob')
    ref: CID
    mime_type: str = Field(..., alias='mimeType')
    size: int

    class Config:
        extra = "forbid"


class UntypedJsonBlobRef(BaseModel):
    cid: str
    mime_type: str = Field(..., alias='mimeType')

    class Config:
        extra = "forbid"


JsonBlobRef = Union[TypedJsonBlobRef, UntypedJsonBlobRef]


class BlobRef:
    def __init__(self, ref: CID, mime_type: str, size: int, original: JsonBlobRef = None):
        self.ref = ref
        self.mime_type = mime_type
        self.size = size
        self.original = original if original else TypedJsonBlobRef(
            ref=ref, mimeType=mime_type, size=size
        )

    @staticmethod
    def as_blob_ref(obj: Dict[Any, Any]) -> Optional[BlobRef]:
        try:
            typed_json_blob_ref = TypedJsonBlobRef(**obj)
            return BlobRef.from_json_ref(typed_json_blob_ref)
        except ValueError:
            try:
                untyped_json_blob_ref = UntypedJsonBlobRef(**obj)
                return BlobRef.from_json_ref(untyped_json_blob_ref)
            except ValueError:
                return None

    @staticmethod
    def from_json_ref(json: JsonBlobRef) -> BlobRef:
        if isinstance(json, TypedJsonBlobRef):
            return BlobRef(json.ref, json.mimeType, json.size)
        else:
            return BlobRef(CID.from_string(json.cid), json.mimeType, -1, json)

    def ipld(self) -> TypedJsonBlobRef:
        return TypedJsonBlobRef(ref=self.ref, mimeType=self.mime_type, size=self.size)

    def to_json(self) -> dict:
        return ipld_to_json(self.ipld())
