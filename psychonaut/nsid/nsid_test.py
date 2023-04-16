import pytest
from .nsid import NSID, InvalidNsidError, ensure_valid_nsid, ensure_valid_nsid_regex


def test_nsid_parsing():
    nsid = NSID.parse("com.example.foo")
    assert nsid.authority == "example.com"
    assert nsid.name == "foo"
    assert str(nsid) == "com.example.foo"

    nsid = NSID.parse("com.example.*")
    assert nsid.authority == "example.com"
    assert nsid.name == "*"
    assert str(nsid) == "com.example.*"

    nsid = NSID.parse("com.long-thing1.cool.fooBarBaz")
    assert nsid.authority == "cool.long-thing1.com"
    assert nsid.name == "fooBarBaz"
    assert str(nsid) == "com.long-thing1.cool.fooBarBaz"


def test_nsid_creation():
    nsid = NSID.create("example.com", "foo")
    assert nsid.authority == "example.com"
    assert nsid.name == "foo"
    assert str(nsid) == "com.example.foo"

    nsid = NSID.create("example.com", "*")
    assert nsid.authority == "example.com"
    assert nsid.name == "*"
    assert str(nsid) == "com.example.*"

    nsid = NSID.create("cool.long-thing1.com", "fooBarBaz")
    assert nsid.authority == "cool.long-thing1.com"
    assert nsid.name == "fooBarBaz"
    assert str(nsid) == "com.long-thing1.cool.fooBarBaz"


def expect_valid(nsid: str):
    ensure_valid_nsid(nsid)
    ensure_valid_nsid_regex(nsid)


def expect_invalid(nsid: str):
    with pytest.raises(InvalidNsidError):
        ensure_valid_nsid(nsid)
    with pytest.raises(InvalidNsidError):
        ensure_valid_nsid_regex(nsid)


def test_nsid_validation():
    expect_valid("com.example.foo")
    long_nsid = "com." + "o" * 63 + ".foo"
    expect_valid(long_nsid)

    too_long_nsid = "com." + "o" * 64 + ".foo"
    expect_invalid(too_long_nsid)

    long_end = "com.example." + "o" * 128
    expect_valid(long_end)

    too_long_end = "com.example." + "o" * 129
    expect_invalid(too_long_end)

    long_overall = "com." + "middle." * 50 + "foo"
    assert len(long_overall) == 357
    expect_valid(long_overall)

    too_long_overall = "com." + "middle." * 100 + "foo"
    assert len(too_long_overall) == 707
    expect_invalid(too_long_overall)

    expect_valid("a.b.c")
    expect_valid("a0.b1.c3")
    expect_valid("a-0.b-1.c-3")
    expect_valid("m.xn--masekowski-d0b.pl")
    expect_valid("one.two.three")

    expect_invalid("example.com")
    expect_invalid("com.example")
    expect_invalid("a.0.c")
    expect_invalid("a.")
    expect_invalid(".one.two.three")
    expect_invalid("one.two.three ")
    expect_invalid("one.two..three")
    expect_invalid("one .two.three")
    expect_invalid(" one.two.three")
    expect_invalid("com.exa💩ple.thing")
    expect_invalid("com.atproto.feed.p@st")
    expect_invalid("com.atproto.feed.p_st")
    expect_invalid("com.atproto.feed.p*st")
    expect_invalid("com.atproto.feed.po#t")
    expect_invalid("com.atproto.feed.p!ot")
    expect_invalid("com.example-.foo")


def test_nsid_onion():
    expect_valid("onion.expyuzz4wqqyqhjn.spec.getThing")
    expect_valid(
        "onion.g2zyxa5ihm7nsggfxnu52rck2vv4rvmdlkiu3zzui5du4xyclen53wid.lex.deleteThing"
    )


def test_nsid_blocks_numeric():
    expect_invalid("org.4chan.lex.getThing")
    expect_invalid("cn.8.lex.stuff")
    expect_invalid(
        "onion.2gzyxa5ihm7nsggfxnu52rck2vv4rvmdlkiu3zzui5du4xyclen53wid.lex.deleteThing"
    )
