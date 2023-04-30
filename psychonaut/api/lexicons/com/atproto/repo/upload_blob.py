from typing import Any
from psychonaut.api.session import Session
from pydantic import BaseModel, Field


class UploadBlobResp(BaseModel):
    blob: Any


class UploadBlobReq(BaseModel):
    """
    Upload a new blob to be added to repo in a later request.
    """

    @property
    def xrpc_id(self) -> str:
        return "com.atproto.repo.uploadBlob"

    async def do_xrpc(self, sess: Session) -> UploadBlobResp:
        resp = await sess.procedure(self)
        return UploadBlobResp(**resp)
