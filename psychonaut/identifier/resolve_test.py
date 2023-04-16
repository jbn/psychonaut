import pytest
from .resolve import resolve_dns, NoHandleRecordError


@pytest.mark.asyncio
async def test_resolve_dns():
    handle = "generativist.xyz"
    expected_did = "did:plc:o32okshy54r5h2vlrjpz3aln"

    did = await resolve_dns(handle)
    assert did == expected_did


@pytest.mark.asyncio
async def test_resolve_dns_no_handle_record_error():
    handle = "nope.generativist.xyz"

    with pytest.raises(NoHandleRecordError):
        await resolve_dns(handle)