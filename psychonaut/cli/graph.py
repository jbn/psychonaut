import json
import click
from psychonaut.api.lexicons.app.bsky.graph.get_followers import (
    GetFollowersReq, GetFollowersResp, get_followers as get_followers_f,
)
from psychonaut.api.lexicons.app.bsky.graph.get_follows import (
    get_follows as get_follows_f, GetFollowsReq, GetFollowsResp,
)
from psychonaut.cli.group import cli
from psychonaut.cli.util import as_async, clean_handle
from psychonaut.client import get_simple_client_session


async def collect_cursored(
    sess,
    req,
    get_fn,
    resp_type,
    collection_k: str,
    cursor_key="cursor",
):
    cursor, last_cursor = None, None
    while True:
        req = req.copy(update={cursor_key: cursor})
        resp = await get_fn(sess, req)
        assert isinstance(resp, resp_type)
        cursor = resp.cursor

        new_items = getattr(resp, collection_k)
        for item in new_items:
            yield item

        if not cursor or cursor == last_cursor or not new_items:
            break

        last_cursor = cursor


@cli.command()
@click.argument("actor")
@as_async
async def get_followers(actor: str):
    actor = clean_handle(actor)

    async with get_simple_client_session() as sess:
        gen = collect_cursored(
            sess,
            GetFollowersReq(actor=actor, limit=100),
            get_followers_f,
            GetFollowersResp,
            "followers"
        )

        async for follower in gen:
            print(json.dumps(follower))


@cli.command()
@click.argument("actor")
@as_async
async def get_follows(actor: str):
    actor = clean_handle(actor)

    async with get_simple_client_session() as sess:
        gen = collect_cursored(
            sess,
            GetFollowsReq(actor=actor, limit=100),
            get_follows_f,
            GetFollowsResp,
            "follows"
        )

        async for follows in gen:
            print(json.dumps(follows))