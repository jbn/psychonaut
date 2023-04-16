from pydantic import BaseModel, Field
from psychonaut.api.session import Session
from typing import Optional, Any


class NotifyOfUpdateReq(BaseModel):
    """
    Notify a crawling service of a recent update. Often when a long break
    between updates causes the connection with the crawling service to
    break.
    """
    hostname: str = Field(..., description='Hostname of the service that is notifying of update.')

    @property
    def xrpc_id(self) -> str:
       return "com.atproto.sync.notifyOfUpdate"


async def notify_of_update(sess: Session, req: NotifyOfUpdateReq) -> Any:
    return await sess.query(req)
