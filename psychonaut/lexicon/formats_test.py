import pytest
from .formats import validate_uri, validate_cid, validate_datetime, validate_nsid, validate_at_identifier


def test_validate_datetime():
    good = [
        "2022-12-12T00:50:36.809Z",
        "2022-12-12T00:50:36Z",
        "2022-12-12T00:50:36.8Z",
        "2022-12-12T00:50:36.80Z",
        "2022-12-12T00:50:36+00:00",
        "2022-12-12T00:50:36.8+00:00",
        "2022-12-11T19:50:36-05:00",
        "2022-12-11T19:50:36.8-05:00",
        "2022-12-11T19:50:36.80-05:00",
        "2022-12-11T19:50:36.809-05:00",
    ]

    for s in good:
        validate_datetime(s)

    with pytest.raises(ValueError):
        assert not validate_datetime("2022-12-12T00:50:36.809")


def test_validate_uri():
    examples = {
        "https://example.com": True,
        "https://example.com/with/path": True,
        "https://example.com/with/path?and=query": True,
        "at://bsky.social": True,
        "did:example:test": True,
        "com.example.uri": False,
    }

    for uri, expected in examples.items():
        if expected:
            validate_uri(uri)
        else:
            with pytest.raises(ValueError):
                validate_uri(uri)


def test_validate_cid():
    validate_cid("bafyreidfayvfuwqa7qlnopdjiqrxzs6blmoeu4rujcjtnci5beludirz2a")
    with pytest.raises(ValueError):
        validate_cid("abapsdofiuwrpoiasdfuaspdfoiu")


def test_validate_nsid():
    validate_nsid("com.atproto.test")

    with pytest.raises(ValueError):
        validate_nsid("com.atproto-.test")


def test_validate_at_identifier():
    examples = {
        'bsky.test': True,
        'did:plc:12345678abcdefghijklmnop': True,    
        'bad id': False,
        '-bad-.test': False,    
    }

    for uri, expected in examples.items():
        if expected:
            validate_at_identifier(uri)
        else:
            with pytest.raises(ValueError):
                validate_at_identifier(uri)
