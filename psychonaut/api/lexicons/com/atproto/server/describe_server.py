from typing import Any, Optional, List
from pydantic import BaseModel, Field
from psychonaut.api.session import Session


class Links(BaseModel):
    """
    [none provided by spec]
    """

    privacyPolicy: Optional[str] = Field(default=None)
    termsOfService: Optional[str] = Field(default=None)


class DescribeServerResp(BaseModel):
    inviteCodeRequired: Optional[bool] = Field(default=None)
    availableUserDomains: List[str] = Field(...)
    links: Optional[Links] = None


class DescribeServerReq(BaseModel):
    """
    Get a document describing the service's accounts configuration.
    """

    @property
    def xrpc_id(self) -> str:
        return "com.atproto.server.describeServer"

    async def do_xrpc(self, sess: Session) -> DescribeServerResp:
        resp = await sess.query(self)
        return DescribeServerResp(**resp)
