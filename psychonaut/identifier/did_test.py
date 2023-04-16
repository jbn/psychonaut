import pytest
from .did import ensure_valid_did, ensure_valid_did_regex, InvalidDidError


def test_did_permissive_validation():
    expect_valid("did:method:val")
    expect_valid("did:method:VAL")
    expect_valid("did:method:val123")
    expect_valid("did:method:123")
    expect_valid("did:method:val-two")
    expect_valid("did:method:val_two")
    expect_valid("did:method:val.two")
    expect_valid("did:method:val:two")
    expect_valid("did:method:val%BB")

    expect_invalid("did")
    expect_invalid("didmethodval")
    expect_invalid("method:did:val")
    expect_invalid("did:method:")
    expect_invalid("didmethod:val")
    expect_invalid("did:methodval")
    expect_invalid(":did:method:val")
    expect_invalid("did.method.val")
    expect_invalid("did:method:val:")
    expect_invalid("did:method:val%")
    expect_invalid("DID:method:val")
    expect_invalid("did:METHOD:val")
    expect_invalid("did:m123:val")

    expect_valid("did:method:" + "v" * 240)
    expect_invalid("did:method:" + "v" * 8500)

    expect_valid("did:m:v")
    expect_valid("did:method::::val")
    expect_valid("did:method:-")
    expect_valid("did:method:-:_:.:%ab")
    expect_valid("did:method:.")
    expect_valid("did:method:_")
    expect_valid("did:method::.")

    expect_invalid("did:method:val/two")
    expect_invalid("did:method:val?two")
    expect_invalid("did:method:val#two")
    expect_invalid("did:method:val%")

    expect_valid("did:onion:2gzyxa5ihm7nsggfxnu52rck2vv4rvmdlkiu3zzui5du4xyclen53wid")


def test_allows_some_real_did_values():
    expect_valid("did:example:123456789abcdefghi")
    expect_valid("did:plc:7iza6de2dwap2sbkpav7c6c6")
    expect_valid("did:web:example.com")
    expect_valid("did:key:zQ3shZc2QzApp2oymGvQbzP8eKheVshBHbU4ZYjeXqwSKEn6N")
    expect_valid("did:ethr:0xb9c5714089478a327f09197987f16f9e5d936e8a")


def expect_valid(h: str):
    ensure_valid_did(h)
    ensure_valid_did_regex(h)


def expect_invalid(h: str):
    with pytest.raises(InvalidDidError):
        ensure_valid_did(h)
    with pytest.raises(InvalidDidError):
        ensure_valid_did_regex(h)
