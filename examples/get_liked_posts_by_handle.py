"""
Example code to download all posts that an actor has Liked from BlueSky
"""

import json
from typing import List

from psychonaut.client import get_simple_client_session
from psychonaut.client.cursors import collect_cursored
from psychonaut.cli.util import as_async, clean_handle

from psychonaut.api.lexicons.com.atproto.identity.resolve_handle import (
    ResolveHandleReq, ResolveHandleResp,
)
from psychonaut.api.lexicons.com.atproto.repo.list_records import (
    ListRecordsReq, ListRecordsResp,
)
from psychonaut.api.lexicons.app.bsky.feed.get_posts import (
    GetPostsReq, GetPostsResp,
)

@as_async
async def resolve_handle(actor: str):

    async with get_simple_client_session() as sess:
        req = ResolveHandleReq(handle=actor)
        resp = await req.do_xrpc(sess)
        assert isinstance(resp, ResolveHandleResp)

        return resp


@as_async
async def list_records(
    user_did: str,
    collection: str,
):
    records = []
    async with get_simple_client_session() as sess:
        gen = collect_cursored(
            sess,
            ListRecordsReq(
                repo=user_did,
                collection=collection,
                limit=100,
            ),
            ListRecordsResp,
            "records"
        )

        async for record in gen:
            records.append(record)
        
        return records


@as_async
async def get_posts(
    uri_list: List[str],
    chunk_size: int = 25,
):
    posts = []
    for i in range(0, len(uri_list), chunk_size):
        uri_chunk = uri_list[i:i+chunk_size]
  
        async with get_simple_client_session() as sess:
            req = GetPostsReq(uris=uri_chunk)
            resp = await req.do_xrpc(sess)
            assert isinstance(resp, GetPostsResp)

            for post in resp.posts:
                posts.append(post)

    return {
        "posts": posts
    }


HANDLE = "somebody.bsky.social"

# Resolve the handle
response = resolve_handle(HANDLE)
print(response)

# Taking the DID from the resolved handle and get all likes by that person
response = list_records(
    user_did=response.did,
    collection="app.bsky.feed.like",
)
uris = []
for record in response:
    print(json.dumps(record, indent=2))
    uris.append(record["value"]["subject"]["uri"])

# Get all like posts
posts = get_posts(
    uri_list = uris,
)
print(json.dumps(posts, indent=2))
