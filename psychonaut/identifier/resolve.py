import asyncio
from typing import Optional
import aiodns


SUBDOMAIN = "_atproto"
PREFIX = "did="


class NoHandleRecordError(Exception):
    pass


async def resolve_dns(
    handle: str, resolver: Optional[aiodns.DNSResolver] = None
) -> str:
    resolver = resolver or aiodns.DNSResolver()

    try:
        resp = await resolver.query(f"{SUBDOMAIN}.{handle}", "TXT")

        first_did = next((r.text for r in resp if r.text.startswith(PREFIX)), None)
        if first_did:
            return first_did[len(PREFIX) :]
    except aiodns.error.DNSError as err:
        if err.args[0] != aiodns.error.ARES_ENOTFOUND:
            raise err
    raise NoHandleRecordError()
