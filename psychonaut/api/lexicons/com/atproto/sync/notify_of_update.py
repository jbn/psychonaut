from typing import Any
from psychonaut.api.session import Session
from pydantic import BaseModel, Field


class NotifyOfUpdateReq(BaseModel):
    """
    Notify a crawling service of a recent update. Often when a long break
    between updates causes the connection with the crawling service to
    break.
    """

    hostname: str = Field(
        ..., description="Hostname of the service that is notifying of update."
    )

    @property
    def xrpc_id(self) -> str:
        return "com.atproto.sync.notifyOfUpdate"

    async def do_xrpc(self, sess: Session) -> Any:
        return await sess.query(self)
