from typing import Any
from psychonaut.api.session import Session
from pydantic import BaseModel, Field


class RequestCrawlReq(BaseModel):
    """
    Request a service to persistently crawl hosted repos.
    """

    hostname: str = Field(
        ..., description="Hostname of the service that is requesting to be crawled."
    )

    @property
    def xrpc_id(self) -> str:
        return "com.atproto.sync.requestCrawl"

    async def do_xrpc(self, sess: Session) -> Any:
        return await sess.query(self)
