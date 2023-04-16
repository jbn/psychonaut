from pydantic import BaseModel, Field
from psychonaut.api.session import Session
from typing import Optional, Any


class RequestCrawlReq(BaseModel):
    """
    Request a service to persistently crawl hosted repos.
    """
    hostname: str = Field(..., description='Hostname of the service that is requesting to be crawled.')

    @property
    def xrpc_id(self) -> str:
       return "com.atproto.sync.requestCrawl"


async def request_crawl(sess: Session, req: RequestCrawlReq) -> Any:
    return await sess.query(req)
