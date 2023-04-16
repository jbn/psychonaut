"""
See:

https://github.com/bluesky-social/atproto/blob/656be937a52688601c088f5aa332137dfaf019cf/packages/lexicon/src/types.ts
"""
from typing import Any, Dict, Union, Optional, List
from pydantic import BaseModel, Field, validator, root_validator
from pydantic import ValidationError as PydanticValidationError
from psychonaut.nsid import NSID


# Primitive types =============================================================

# TODO: forbid extra?


class LexBoolean(BaseModel):
    type: str = Field("boolean", const=True)
    description: Optional[str]
    default: Optional[bool]
    const: Optional[bool]


class LexInteger(BaseModel):
    type: str = Field("integer", const=True)
    description: Optional[str]
    default: Optional[int]
    minimum: Optional[int]
    maximum: Optional[int]
    enum: Optional[List[int]]
    const: Optional[int]


class LexStringFormat(str):
    datetime = "datetime"
    uri = "uri"
    at_uri = "at-uri"
    did = "did"
    handle = "handle"
    at_identifier = "at-identifier"
    nsid = "nsid"
    cid = "cid"


class LexString(BaseModel):
    type: str = Field("string", const=True)
    format: Optional[LexStringFormat]
    description: Optional[str]
    default: Optional[str]
    min_length: Optional[int] = Field(None, alias="minLength")
    max_length: Optional[int] = Field(None, alias="maxLength")
    min_graphemes: Optional[int] = Field(None, alias="minGraphemes")
    max_graphemes: Optional[int] = Field(None, alias="maxGraphemes")
    enum: Optional[List[str]]
    const: Optional[str]
    known_values: Optional[List[str]] = Field(None, alias="knownValues")


class LexUnknown(BaseModel):
    type: str = Field("unknown", const=True)
    description: Optional[str]


LexPrimitive = Union[LexBoolean, LexInteger, LexString, LexUnknown]

# ip1d types ==================================================================


class LexBytes(BaseModel):
    type: str = Field("bytes", const=True)
    description: Optional[str]
    maxLength: Optional[int]
    minLength: Optional[int]


class LexCidLink(BaseModel):
    type: str = Field("cid-link", const=True)
    description: Optional[str]


LexIpldType = Union[LexBytes, LexCidLink]


# reference types =============================================================


class LexRef(BaseModel):
    type: str = Field("ref", const=True)
    description: Optional[str]
    ref: str


class LexRefUnion(BaseModel):
    type: str = Field("union", const=True)
    description: Optional[str]
    refs: List[str]
    closed: Optional[bool]


LexRefVariant = Union[LexRef, LexRefUnion]

# blob types ==================================================================


class LexBlob(BaseModel):
    type: str = Field("blob", const=True)
    description: Optional[str]
    accept: Optional[List[str]]
    maxSize: Optional[int]


# complex types ===============================================================


class LexArray(BaseModel):
    type: str = Field("array", const=True)
    description: Optional[str]
    items: Union[LexPrimitive, LexIpldType, LexBlob, LexRefVariant]
    min_length: Optional[int] = Field(None, alias="minLength")
    max_length: Optional[int] = Field(None, alias="maxLength")


class LexPrimitiveArray(LexArray):
    items: LexPrimitive


class LexToken(BaseModel):
    type: str = Field("token", const=True)
    description: Optional[str]


class LexObject(BaseModel):
    type: str = Field("object", const=True)
    description: Optional[str]
    required: Optional[List[str]]
    nullable: Optional[List[str]]
    properties: Optional[
        dict[str, Union[LexRefVariant, LexIpldType, LexArray, LexBlob, LexPrimitive]]
    ]


# xrpc types =================================================================


class LexXrpcParameters(BaseModel):
    type: str = Field("params", const=True)
    description: Optional[str]
    required: Optional[List[str]]
    properties: dict[str, Union[LexPrimitive, LexPrimitiveArray]]


class LexXrpcBody(BaseModel):
    description: Optional[str]
    encoding: str
    schema_kludge: Optional[Union[LexRefVariant, LexObject]] = Field(
        None, alias="schema"
    )


class LexXrpcSubscriptionMessage(BaseModel):
    description: Optional[str]
    schema_kludge: Optional[Union[LexRefVariant, LexObject]] = Field(
        None, alias="schema"
    )


class LexXrpcError(BaseModel):
    name: str
    description: Optional[str]


class LexXrpcQuery(BaseModel):
    type: str = Field("query", const=True)
    description: Optional[str]
    parameters: Optional[LexXrpcParameters]
    output: Optional[LexXrpcBody]
    errors: Optional[List[LexXrpcError]]


class LexXrpcProcedure(BaseModel):
    type: str = Field("procedure", const=True)
    description: Optional[str]
    parameters: Optional[LexXrpcParameters]
    input: Optional[LexXrpcBody]
    output: Optional[LexXrpcBody]
    errors: Optional[List[LexXrpcError]]


class LexXrpcSubscription(BaseModel):
    type: str = Field("subscription", const=True)
    description: Optional[str]
    parameters: Optional[LexXrpcParameters]
    message: Optional[LexXrpcSubscriptionMessage]
    infos: Optional[List[LexXrpcError]]
    errors: Optional[List[LexXrpcError]]


# database types ==============================================================


class LexRecord(BaseModel):
    type: str = Field("record", const=True)
    description: Optional[str]
    key: Optional[str]
    record: LexObject


# core types ==================================================================


LexUserType = Union[
    LexRecord,
    LexXrpcQuery,
    LexXrpcProcedure,
    LexXrpcSubscription,
    LexBlob,
    LexArray,
    LexToken,
    LexObject,
    LexBoolean,
    LexInteger,
    LexString,
    LexBytes,
    LexCidLink,
    LexUnknown,
]

_lex_user_type_to_type = {
    "record": LexRecord,
    "query": LexXrpcQuery,
    "procedure": LexXrpcProcedure,
    "subscription": LexXrpcSubscription,
    "blob": LexBlob,
    "array": LexArray,
    "token": LexToken,
    "object": LexObject,
    "boolean": LexBoolean,
    "integer": LexInteger,
    "string": LexString,
    "bytes": LexBytes,
    "cid-link": LexCidLink,
    "unknown": LexUnknown,
}


class LexiconDoc(BaseModel):
    lexicon: int = Field(1, const=True)
    id: str
    revision: Optional[int]
    description: Optional[str]
    defs: dict[str, LexUserType]

    @root_validator
    def validate_main_definition(cls, values):
        defs = values.get("defs")
        if defs:
            for def_id, def_ in defs.items():
                if def_id != "main" and (
                    def_.type == "record"
                    or def_.type == "procedure"
                    or def_.type == "query"
                    or def_.type == "subscription"
                ):
                    raise ValidationError(
                        "Records, procedures, queries, and subscriptions must be the main definition."
                    )
        return values

    @validator("id")
    def validate_nsid(cls, value):
        if not NSID.is_valid(value):
            raise ValidationError("Must be a valid NSID")
        return value

    def __init__(self, **data):
        if "defs" in data:
            data["defs"] = {
                k: _lex_user_type_to_type[v["type"]].parse_obj(v)
                for k, v in data["defs"].items()
            }
        super().__init__(**data)


# helpers =====================================================================


def is_valid_lexicon_doc(value: Any) -> bool:
    try:
        LexiconDoc.parse_obj(value)
        return True
    except PydanticValidationError:
        return False


def is_obj(obj: Any) -> bool:
    return obj is not None and isinstance(obj, dict)


def has_prop(data: Dict, prop: str) -> bool:
    return prop in data


class DiscriminatedObject(BaseModel):
    __root__: Dict[str, Any]

    @validator("__root__")
    def check_type(cls, value):
        if "$type" not in value:
            raise ValueError("DiscriminatedObject must have a $type property")
        return value


def is_discriminated_object(value: Any) -> bool:
    try:
        DiscriminatedObject.parse_obj(value)
        return True
    except ValueError:
        return False


class LexiconDocMalformedError(Exception):
    def __init__(self, message: str, schema_def: Any, issues: Optional[List] = None):
        super().__init__(message)
        self.schema_def = schema_def
        self.issues = issues


class ValidationResult:
    def __init__(
        self, success: bool, value: Optional[Any] = None, error: Optional[Any] = None
    ):
        self.success = success
        self.value = value
        self.error = error


class ValidationError(Exception):
    pass


class InvalidLexiconError(Exception):
    pass


class LexiconDefNotFoundError(Exception):
    pass
