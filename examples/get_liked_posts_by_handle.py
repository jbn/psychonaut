import asyncio
import json
import sys
from more_itertools import chunked

from psychonaut.client import get_simple_client_session
from psychonaut.client.cursors import collect_cursored
from psychonaut.cli.util import clean_handle

from psychonaut.api.lexicons.com.atproto.identity.resolve_handle import ResolveHandleReq
from psychonaut.api.lexicons.com.atproto.repo.list_records import (
    ListRecordsReq,
    ListRecordsResp,
)
from psychonaut.api.lexicons.app.bsky.feed.get_posts import GetPostsReq


async def main(handle: str):
    async with get_simple_client_session() as sess:
        # Resolve the handle
        response = await ResolveHandleReq(handle=handle).do_xrpc(sess)
        print(response)

        # Taking the DID from the resolved handle and get all likes by that person
        likes = [
            record
            async for record in collect_cursored(
                sess,
                ListRecordsReq(
                    repo=response.did,
                    collection="app.bsky.feed.like",
                    limit=100,
                ),
                ListRecordsResp,
                "records",
            )
        ]

        uris = []
        for record in likes:
            print(json.dumps(record, indent=2))
            uris.append(
            # TODO: update after fixing ref bug that makes these Any types
                record["value"]["subject"]["uri"]
            )  

        # Get all liked posts
        posts = [
            post
            for uri_chunk in chunked(uris, 25)
            for post in await GetPostsReq(uris=uri_chunk).do_xrpc(sess)
        ]

        print(json.dumps({"posts": posts}, indent=2))


if __name__ == "__main__":
    handle = sys.argv[1]
    asyncio.run(main(clean_handle(handle)))
