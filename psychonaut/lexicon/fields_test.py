from psychonaut.lexicon.ctx import GenCtx
from .types import LexArray, LexInteger, LexBoolean, LexString
from .fields import _generate_array_field, _generate_integer_field, _generate_bool_field, _generate_str_field


def test_generate_integer_field():
    opts = {
        "type": "integer",
        "default": 50,
        "minimum": 1,
        "maximum": 100,
    }

    example = LexInteger(**opts)
    s = _generate_integer_field("test_k", True, example)
    assert s == "test_k: int = Field(default=50, ge=1, le=100)"
    s = _generate_integer_field("test_k", False, example)
    assert s == "test_k: Optional[int] = Field(default=50, ge=1, le=100)"

    opts["description"] = "a description"
    example = LexInteger(**opts)
    s = _generate_integer_field("test_k", True, example)
    expected = (
        "test_k: int = Field(default=50, description='a description', ge=1, le=100)"
    )
    assert s == expected


def test_generate_bool_field():
    opts = {"type": "boolean"}

    example = LexBoolean(**opts)
    s = _generate_bool_field("test_k", True, example)
    assert s == "test_k: bool = Field(...)"

    opts["default"] = True
    example = LexBoolean(**opts)
    s = _generate_bool_field("test_k", True, example)
    assert s == "test_k: bool = Field(default=True)"


def test_generate_str_field():
    opts = {"type": "string", "description": "The DID of the repo."}

    ctx, example = GenCtx(), LexString(**opts)
    s = _generate_str_field(ctx, "test_k", True, example)
    assert s == "test_k: str = Field(..., description='The DID of the repo.')"

    opts["knownValues"] = ["recent", "usage"]
    del opts["description"]
    ctx, example = GenCtx(), LexString(**opts)
    s = _generate_str_field(ctx, "test_k", True, example)
    assert s == "test_k: str = Field(..., known_values=['recent', 'usage'])"

    opts["format"] = "cid"
    del opts["knownValues"]
    ctx, example = GenCtx(), LexString(**opts)
    s = _generate_str_field(ctx, "test_k", True, example)
    assert s == "test_k: str = Field(..., pre=True, validator=validate_cid)"

    opts["format"] = "did"
    ctx, example = GenCtx(), LexString(**opts)
    s = _generate_str_field(ctx, "test_k", True, example)
    assert s == "test_k: str = Field(..., pre=True, validator=validate_did)"

    opts["format"] = "handle"
    ctx, example = GenCtx(), LexString(**opts)
    s = _generate_str_field(ctx, "test_k", True, example)
    assert s == "test_k: str = Field(..., pre=True, validator=validate_handle)"


def test_generate_array_field():
    opts = {
        "type": "array",
        "description": "a desc",
        "items": {
            "type": "string",
            "format": "did",
        },
    }
    ctx, example = GenCtx(), LexArray(**opts)
    s = _generate_array_field(ctx, "test_k", True, example)
    assert s == "test_k: List[str] = Field(..., description='a desc', pre=True, validator=validate_array(validate_did))"
