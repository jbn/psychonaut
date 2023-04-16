import pytest
from psychonaut.uri import AtUri, parse, parse_relative
from psychonaut.uri.validation import ensure_valid_at_uri, ensure_valid_at_uri_regex

URI_TESTS = [
    ["foo.com", "foo.com", "", "", ""],
    ["at://foo.com", "foo.com", "", "", ""],
    ["at://foo.com/", "foo.com", "/", "", ""],
    ["at://foo.com/foo", "foo.com", "/foo", "", ""],
    ["at://foo.com/foo/", "foo.com", "/foo/", "", ""],
    ["at://foo.com/foo/bar", "foo.com", "/foo/bar", "", ""],
    ["at://foo.com?foo=bar", "foo.com", "", "foo=bar", ""],
    ["at://foo.com?foo=bar&baz=buux", "foo.com", "", "foo=bar&baz=buux", ""],
    ["at://foo.com/?foo=bar", "foo.com", "/", "foo=bar", ""],
    ["at://foo.com/foo?foo=bar", "foo.com", "/foo", "foo=bar", ""],
    ["at://foo.com/foo/?foo=bar", "foo.com", "/foo/", "foo=bar", ""],
    ["at://foo.com#hash", "foo.com", "", "", "#hash"],
    ["at://foo.com/#hash", "foo.com", "/", "", "#hash"],
    ["at://foo.com/foo#hash", "foo.com", "/foo", "", "#hash"],
    ["at://foo.com/foo/#hash", "foo.com", "/foo/", "", "#hash"],
    ["at://foo.com?foo=bar#hash", "foo.com", "", "foo=bar", "#hash"],
    [
        "did:example:EiAnKD8-jfdd0MDcZUjAbRgaThBrMxPTFOxcnfJhI7Ukaw",
        "did:example:EiAnKD8-jfdd0MDcZUjAbRgaThBrMxPTFOxcnfJhI7Ukaw",
        "",
        "",
        "",
    ],
    [
        "at://did:example:EiAnKD8-jfdd0MDcZUjAbRgaThBrMxPTFOxcnfJhI7Ukaw",
        "did:example:EiAnKD8-jfdd0MDcZUjAbRgaThBrMxPTFOxcnfJhI7Ukaw",
        "",
        "",
        "",
    ],
    [
        "at://did:example:EiAnKD8-jfdd0MDcZUjAbRgaThBrMxPTFOxcnfJhI7Ukaw/",
        "did:example:EiAnKD8-jfdd0MDcZUjAbRgaThBrMxPTFOxcnfJhI7Ukaw",
        "/",
        "",
        "",
    ],
    [
        "at://did:example:EiAnKD8-jfdd0MDcZUjAbRgaThBrMxPTFOxcnfJhI7Ukaw/foo",
        "did:example:EiAnKD8-jfdd0MDcZUjAbRgaThBrMxPTFOxcnfJhI7Ukaw",
        "/foo",
        "",
        "",
    ],
    [
        "at://did:example:EiAnKD8-jfdd0MDcZUjAbRgaThBrMxPTFOxcnfJhI7Ukaw/foo/",
        "did:example:EiAnKD8-jfdd0MDcZUjAbRgaThBrMxPTFOxcnfJhI7Ukaw",
        "/foo/",
        "",
        "",
    ],
    [
        "at://did:example:EiAnKD8-jfdd0MDcZUjAbRgaThBrMxPTFOxcnfJhI7Ukaw/foo/bar",
        "did:example:EiAnKD8-jfdd0MDcZUjAbRgaThBrMxPTFOxcnfJhI7Ukaw",
        "/foo/bar",
        "",
        "",
    ],
    [
        "at://did:example:EiAnKD8-jfdd0MDcZUjAbRgaThBrMxPTFOxcnfJhI7Ukaw?foo=bar",
        "did:example:EiAnKD8-jfdd0MDcZUjAbRgaThBrMxPTFOxcnfJhI7Ukaw",
        "",
        "foo=bar",
        "",
    ],
    [
        "at://did:example:EiAnKD8-jfdd0MDcZUjAbRgaThBrMxPTFOxcnfJhI7Ukaw?foo=bar&baz=buux",
        "did:example:EiAnKD8-jfdd0MDcZUjAbRgaThBrMxPTFOxcnfJhI7Ukaw",
        "",
        "foo=bar&baz=buux",
        "",
    ],
    [
        "at://did:example:EiAnKD8-jfdd0MDcZUjAbRgaThBrMxPTFOxcnfJhI7Ukaw/?foo=bar",
        "did:example:EiAnKD8-jfdd0MDcZUjAbRgaThBrMxPTFOxcnfJhI7Ukaw",
        "/",
        "foo=bar",
        "",
    ],
    [
        "at://did:example:EiAnKD8-jfdd0MDcZUjAbRgaThBrMxPTFOxcnfJhI7Ukaw/foo?foo=bar",
        "did:example:EiAnKD8-jfdd0MDcZUjAbRgaThBrMxPTFOxcnfJhI7Ukaw",
        "/foo",
        "foo=bar",
        "",
    ],
    [
        "at://did:example:EiAnKD8-jfdd0MDcZUjAbRgaThBrMxPTFOxcnfJhI7Ukaw/foo/?foo=bar",
        "did:example:EiAnKD8-jfdd0MDcZUjAbRgaThBrMxPTFOxcnfJhI7Ukaw",
        "/foo/",
        "foo=bar",
        "",
    ],
    [
        "at://did:example:EiAnKD8-jfdd0MDcZUjAbRgaThBrMxPTFOxcnfJhI7Ukaw#hash",
        "did:example:EiAnKD8-jfdd0MDcZUjAbRgaThBrMxPTFOxcnfJhI7Ukaw",
        "",
        "",
        "#hash",
    ],
    [
        "at://did:example:EiAnKD8-jfdd0MDcZUjAbRgaThBrMxPTFOxcnfJhI7Ukaw/#hash",
        "did:example:EiAnKD8-jfdd0MDcZUjAbRgaThBrMxPTFOxcnfJhI7Ukaw",
        "/",
        "",
        "#hash",
    ],
    [
        "at://did:example:EiAnKD8-jfdd0MDcZUjAbRgaThBrMxPTFOxcnfJhI7Ukaw/foo#hash",
        "did:example:EiAnKD8-jfdd0MDcZUjAbRgaThBrMxPTFOxcnfJhI7Ukaw",
        "/foo",
        "",
        "#hash",
    ],
    [
        "at://did:example:EiAnKD8-jfdd0MDcZUjAbRgaThBrMxPTFOxcnfJhI7Ukaw/foo/#hash",
        "did:example:EiAnKD8-jfdd0MDcZUjAbRgaThBrMxPTFOxcnfJhI7Ukaw",
        "/foo/",
        "",
        "#hash",
    ],
    [
        "at://did:example:EiAnKD8-jfdd0MDcZUjAbRgaThBrMxPTFOxcnfJhI7Ukaw?foo=bar#hash",
        "did:example:EiAnKD8-jfdd0MDcZUjAbRgaThBrMxPTFOxcnfJhI7Ukaw",
        "",
        "foo=bar",
        "#hash",
    ],
    ["did:web:localhost%3A1234", "did:web:localhost%3A1234", "", "", ""],
    ["at://did:web:localhost%3A1234", "did:web:localhost%3A1234", "", "", ""],
    [
        "at://did:web:localhost%3A1234/",
        "did:web:localhost%3A1234",
        "/",
        "",
        "",
    ],
    [
        "at://did:web:localhost%3A1234/foo",
        "did:web:localhost%3A1234",
        "/foo",
        "",
        "",
    ],
    [
        "at://did:web:localhost%3A1234/foo/",
        "did:web:localhost%3A1234",
        "/foo/",
        "",
        "",
    ],
    [
        "at://did:web:localhost%3A1234/foo/bar",
        "did:web:localhost%3A1234",
        "/foo/bar",
        "",
        "",
    ],
    [
        "at://did:web:localhost%3A1234?foo=bar",
        "did:web:localhost%3A1234",
        "",
        "foo=bar",
        "",
    ],
    [
        "at://did:web:localhost%3A1234?foo=bar&baz=buux",
        "did:web:localhost%3A1234",
        "",
        "foo=bar&baz=buux",
        "",
    ],
    [
        "at://did:web:localhost%3A1234/?foo=bar",
        "did:web:localhost%3A1234",
        "/",
        "foo=bar",
        "",
    ],
    [
        "at://did:web:localhost%3A1234/foo?foo=bar",
        "did:web:localhost%3A1234",
        "/foo",
        "foo=bar",
        "",
    ],
    [
        "at://did:web:localhost%3A1234/foo/?foo=bar",
        "did:web:localhost%3A1234",
        "/foo/",
        "foo=bar",
        "",
    ],
    [
        "at://did:web:localhost%3A1234#hash",
        "did:web:localhost%3A1234",
        "",
        "",
        "#hash",
    ],
    [
        "at://did:web:localhost%3A1234/#hash",
        "did:web:localhost%3A1234",
        "/",
        "",
        "#hash",
    ],
    [
        "at://did:web:localhost%3A1234/foo#hash",
        "did:web:localhost%3A1234",
        "/foo",
        "",
        "#hash",
    ],
    [
        "at://did:web:localhost%3A1234/foo/#hash",
        "did:web:localhost%3A1234",
        "/foo/",
        "",
        "#hash",
    ],
    [
        "at://did:web:localhost%3A1234?foo=bar#hash",
        "did:web:localhost%3A1234",
        "",
        "foo=bar",
        "#hash",
    ],
    [
        "at://4513echo.bsky.social/app.bsky.feed.post/3jsrpdyf6ss23",
        "4513echo.bsky.social",
        "/app.bsky.feed.post/3jsrpdyf6ss23",
        "",
        "",
    ],
]
# TODO: I should make all of the tests as json and make a suite for anyone


class TestAtURLS:
    @pytest.mark.parametrize("uri,hostname,pathname,search,hash", URI_TESTS)
    def test_parse(self, uri, hostname, pathname, search, hash):
        urip = AtUri(uri)
        assert urip.protocol == "at:"
        assert urip.host == hostname
        assert urip.hostname == hostname
        assert urip.origin == f"at://{hostname}"
        assert urip.pathname == pathname
        assert urip.search == search, urip.search_params
        assert urip.hash == hash

    @pytest.mark.parametrize(
        "uri,collection,rkey",
        [
            ("at://foo.com", "", ""),
            ("at://foo.com/com.example.foo", "com.example.foo", ""),
            ("at://foo.com/com.example.foo/123", "com.example.foo", "123"),
        ],
    )
    def test_handles_atp_specific_parsing(self, uri, collection, rkey):
        urip = AtUri(uri)
        assert urip.collection == collection
        assert urip.rkey == rkey

    def test_supports_modifications(self):
        urip = AtUri("at://foo.com")
        assert str(urip) == "at://foo.com/"

        urip.host = "bar.com"
        assert str(urip) == "at://bar.com/"
        urip.host = "did:web:localhost%3A1234"
        assert str(urip) == "at://did:web:localhost%3A1234/"
        urip.host = "foo.com"

        urip.pathname = "/"
        assert str(urip) == "at://foo.com/"
        urip.pathname = "/foo"
        assert str(urip) == "at://foo.com/foo"
        urip.pathname = "foo"
        assert str(urip) == "at://foo.com/foo"

        urip.collection = "com.example.foo"
        urip.rkey = "123"
        assert str(urip) == "at://foo.com/com.example.foo/123"
        urip.rkey = "124"
        assert str(urip) == "at://foo.com/com.example.foo/124"
        urip.collection = "com.other.foo"
        assert str(urip) == "at://foo.com/com.other.foo/124"
        urip.pathname = ""
        urip.rkey = "123"
        assert str(urip) == "at://foo.com/undefined/123"
        urip.pathname = "foo"

        urip.search = "?foo=bar"
        assert str(urip) == "at://foo.com/foo?foo=bar"
        urip.search_params["baz"] = ["buux"]
        assert str(urip) == "at://foo.com/foo?foo=bar&baz=buux"

        urip.hash = "#hash"
        assert str(urip) == "at://foo.com/foo?foo=bar&baz=buux#hash"
        urip.hash = "hash"
        assert str(urip) == "at://foo.com/foo?foo=bar&baz=buux#hash"

    @pytest.mark.parametrize(
        "base",
        [
            "did:web:localhost%3A1234",
            "at://did:web:localhost%3A1234",
            "at://did:web:localhost%3A1234/foo/bar?foo=bar&baz=buux#hash",
            "did:web:localhost%3A1234",
            "at://did:web:localhost%3A1234",
            "at://did:web:localhost%3A1234/foo/bar?foo=bar&baz=buux#hash",
        ],
    )
    def test_supports_relative_uris(self, base):
        tests = [
            ("", "", "", ""),
            ("/", "/", "", ""),
            ("/foo", "/foo", "", ""),
            ("/foo/", "/foo/", "", ""),
            ("/foo/bar", "/foo/bar", "", ""),
            ("?foo=bar", "", "foo=bar", ""),
            ("?foo=bar&baz=buux", "", "foo=bar&baz=buux", ""),
            ("/?foo=bar", "/", "foo=bar", ""),
            ("/foo?foo=bar", "/foo", "foo=bar", ""),
            ("/foo/?foo=bar", "/foo/", "foo=bar", ""),
            ("#hash", "", "", "#hash"),
            ("/#hash", "/", "", "#hash"),
            ("/foo#hash", "/foo", "", "#hash"),
            ("/foo/#hash", "/foo/", "", "#hash"),
            ("?foo=bar#hash", "", "foo=bar", "#hash"),
        ]
        basep = AtUri(base)
        for relative, pathname, search, hash in tests:
            urip = AtUri(relative, base)
            assert urip.protocol == "at:"
            assert urip.host == basep.host
            assert urip.hostname == basep.hostname
            assert urip.origin == basep.origin
            assert urip.pathname == pathname
            assert urip.search == search
            assert urip.hash == hash


# at url ======================================================================


def expect_valid_at(h):
    ensure_valid_at_uri(h)
    ensure_valid_at_uri_regex(h)


def expect_invalid_at(h):
    with pytest.raises(Exception):
        ensure_valid_at_uri(h)
    with pytest.raises(Exception):
        ensure_valid_at_uri_regex(h)


class TestAtUrlValidation:
    def test_spec_basics(self):
        expect_valid_at("at://did:plc:asdf123")
        expect_valid_at("at://user.bsky.social")
        expect_valid_at("at://did:plc:asdf123/com.atproto.feed.post")
        expect_valid_at("at://did:plc:asdf123/com.atproto.feed.post/record")

        expect_valid_at("at://did:plc:asdf123#/frag")
        expect_valid_at("at://user.bsky.social#/frag")
        expect_valid_at("at://did:plc:asdf123/com.atproto.feed.post#/frag")
        expect_valid_at("at://did:plc:asdf123/com.atproto.feed.post/record#/frag")

        expect_invalid_at("a://did:plc:asdf123")
        expect_invalid_at("at//did:plc:asdf123")
        expect_invalid_at("at:/a/did:plc:asdf123")
        expect_invalid_at("at:/did:plc:asdf123")
        expect_invalid_at("AT://did:plc:asdf123")
        expect_invalid_at("http://did:plc:asdf123")
        expect_invalid_at("://did:plc:asdf123")
        expect_invalid_at("at:did:plc:asdf123")
        expect_invalid_at("at:/did:plc:asdf123")
        expect_invalid_at("at:///did:plc:asdf123")
        expect_invalid_at("at://:/did:plc:asdf123")
        expect_invalid_at("at:/ /did:plc:asdf123")
        expect_invalid_at("at://did:plc:asdf123 ")
        expect_invalid_at("at://did:plc:asdf123/ ")
        expect_invalid_at(" at://did:plc:asdf123")
        expect_invalid_at("at://did:plc:asdf123/com.atproto.feed.post ")
        expect_invalid_at("at://did:plc:asdf123/com.atproto.feed.post# ")
        expect_invalid_at("at://did:plc:asdf123/com.atproto.feed.post#/ ")
        expect_invalid_at("at://did:plc:asdf123/com.atproto.feed.post#/frag ")
        expect_invalid_at("at://did:plc:asdf123/com.atproto.feed.post#fr ag")
        expect_invalid_at("//did:plc:asdf123")
        expect_invalid_at("at://name")
        expect_invalid_at("at://name.0")
        expect_invalid_at("at://diD:plc:asdf123")
        expect_invalid_at("at://did:plc:asdf123/com.atproto.feed.p@st")
        expect_invalid_at("at://did:plc:asdf123/com.atproto.feed.p$st")
        expect_invalid_at("at://did:plc:asdf123/com.atproto.feed.p%st")
        expect_invalid_at("at://did:plc:asdf123/com.atproto.feed.p&st")
        expect_invalid_at("at://did:plc:asdf123/com.atproto.feed.p()t")
        expect_invalid_at("at://did:plc:asdf123/com.atproto.feed_post")
        expect_invalid_at("at://did:plc:asdf123/-com.atproto.feed.post")
        expect_invalid_at("at://did:plc:asdf@123/com.atproto.feed.post")

        expect_invalid_at("at://DID:plc:asdf123")
        expect_invalid_at("at://user.bsky.123")
        expect_invalid_at("at://bsky")
        expect_invalid_at("at://did:plc:")
        expect_invalid_at("at://did:plc:")
        expect_invalid_at("at://frag")

        expect_valid_at("at://did:plc:asdf123/com.atproto.feed.post/" + "o" * 800)
        expect_invalid_at(
            "at://did:plc:asdf123/com.atproto.feed.post/" + "o" * 8200,
        )

    def test_edge_cases(self):
        expect_invalid_at("at://user.bsky.social//")
        expect_invalid_at("at://user.bsky.social//com.atproto.feed.post")

        expect_invalid_at("at://user.bsky.social/com.atproto.feed.post//")
        expect_invalid_at(
            "at://did:plc:asdf123/com.atproto.feed.post/asdf123/more/more"
        )

        expect_invalid_at("at://did:plc:asdf123/short/stuff")
        expect_invalid_at("at://did:plc:asdf123/12345")

    def test_no_trailing_slashes(self):
        expect_valid_at("at://did:plc:asdf123")
        expect_invalid_at("at://did:plc:asdf123/")

        expect_valid_at("at://user.bsky.social")
        expect_invalid_at("at://user.bsky.social/")

        expect_valid_at("at://did:plc:asdf123/com.atproto.feed.post")
        expect_invalid_at("at://did:plc:asdf123/com.atproto.feed.post/")

        expect_valid_at("at://did:plc:asdf123/com.atproto.feed.post/record")
        expect_invalid_at("at://did:plc:asdf123/com.atproto.feed.post/record/")
        expect_invalid_at("at://did:plc:asdf123/com.atproto.feed.post/record/#/frag")

    def test_strict_paths(self):
        expect_valid_at("at://did:plc:asdf123/com.atproto.feed.post/asdf123")
        expect_invalid_at("at://did:plc:asdf123/com.atproto.feed.post/asdf123/asdf")

    def test_permissive_record_keys(self):
        expect_valid_at("at://did:plc:asdf123/com.atproto.feed.post/asdf123")
        expect_valid_at("at://did:plc:asdf123/com.atproto.feed.post/a")
        expect_valid_at("at://did:plc:asdf123/com.atproto.feed.post/%23")

        expect_valid_at("at://did:plc:asdf123/com.atproto.feed.post/$@!*)(:,;~.sdf123")
        expect_valid_at("at://did:plc:asdf123/com.atproto.feed.post/~'sdf123")

        expect_valid_at("at://did:plc:asdf123/com.atproto.feed.post/$")
        expect_valid_at("at://did:plc:asdf123/com.atproto.feed.post/@")
        expect_valid_at("at://did:plc:asdf123/com.atproto.feed.post/!")
        expect_valid_at("at://did:plc:asdf123/com.atproto.feed.post/*")
        expect_valid_at("at://did:plc:asdf123/com.atproto.feed.post/(")
        expect_valid_at("at://did:plc:asdf123/com.atproto.feed.post/,")
        expect_valid_at("at://did:plc:asdf123/com.atproto.feed.post/;")
        expect_valid_at("at://did:plc:asdf123/com.atproto.feed.post/abc%30123")

    def test_url_encoding(self):
        expect_valid_at("at://did:plc:asdf123/com.atproto.feed.post/%30")
        expect_valid_at("at://did:plc:asdf123/com.atproto.feed.post/%3")
        expect_valid_at("at://did:plc:asdf123/com.atproto.feed.post/%")
        expect_valid_at("at://did:plc:asdf123/com.atproto.feed.post/%zz")
        expect_valid_at("at://did:plc:asdf123/com.atproto.feed.post/%%%")

    def test_fragments(self):
        expect_valid_at("at://did:plc:asdf123#/frac")

        expect_invalid_at("at://did:plc:asdf123#")
        expect_invalid_at("at://did:plc:asdf123##")
        expect_invalid_at("#at://did:plc:asdf123")
        expect_invalid_at("at://did:plc:asdf123#/asdf#/asdf")

        expect_valid_at("at://did:plc:asdf123#/com.atproto.feed.post")
        expect_valid_at("at://did:plc:asdf123#/com.atproto.feed.post/")
        expect_valid_at("at://did:plc:asdf123#/asdf/")

        expect_valid_at("at://did:plc:asdf123/com.atproto.feed.post#/$@!*():,;~.sdf123")
        expect_valid_at("at://did:plc:asdf123#/[asfd]")

        expect_valid_at("at://did:plc:asdf123#/$")
        expect_valid_at("at://did:plc:asdf123#/*")
        expect_valid_at("at://did:plc:asdf123#/;")
        expect_valid_at("at://did:plc:asdf123#/,")
