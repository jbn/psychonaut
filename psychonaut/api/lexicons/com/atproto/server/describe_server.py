from pydantic import BaseModel, Field
from typing import Optional, List, Any
from psychonaut.api.session import Session


class DescribeServerReq(BaseModel):
    """
    Get a document describing the service's accounts configuration.
    """

    @property
    def xrpc_id(self) -> str:
       return "com.atproto.server.describeServer"


class DescribeServerResp(BaseModel):
    inviteCodeRequired: Optional[bool] = Field(default=None)
    availableUserDomains: List[str] = Field(...)
    links: Optional[Any] = None

    @property
    def xrpc_id(self) -> str:
       return "com.atproto.server.describeServer"


async def describe_server(sess: Session, req: DescribeServerReq) -> DescribeServerResp:
    resp = await sess.query(req)
    return DescribeServerResp(**resp)
