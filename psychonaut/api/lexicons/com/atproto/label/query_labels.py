from pydantic import BaseModel, Field
from typing import Optional, List, Any
from psychonaut.lexicon.formats import validate_did, validate_array
from psychonaut.api.session import Session


class QueryLabelsReq(BaseModel):
    """
    Find labels relevant to the provided URI patterns.
    """
    uriPatterns: List[str] = Field(..., description="List of AT URI patterns to match (boolean 'OR'). Each may be a prefix (ending with '*'; will match inclusive of the string leading to '*'), or a full URI")
    sources: Optional[List[str]] = Field(default=None, description='Optional list of label sources (DIDs) to filter on', pre=True, validator=validate_array(validate_did))
    limit: Optional[int] = Field(default=50, ge=1, le=250)
    cursor: Optional[str] = Field(default=None)

    @property
    def xrpc_id(self) -> str:
       return "com.atproto.label.queryLabels"


class QueryLabelsResp(BaseModel):
    cursor: Optional[str] = Field(default=None)
    labels: Any

    @property
    def xrpc_id(self) -> str:
       return "com.atproto.label.queryLabels"


async def query_labels(sess: Session, req: QueryLabelsReq) -> QueryLabelsResp:
    resp = await sess.query(req)
    return QueryLabelsResp(**resp)
