import json
import click
from psychonaut.api.lexicons.app.bsky.graph.get_followers import (
    GetFollowersReq, GetFollowersResp
)
from psychonaut.api.lexicons.app.bsky.graph.get_follows import (
    GetFollowsReq, GetFollowsResp,
)
from psychonaut.cli.group import cli
from psychonaut.cli.util import as_async, clean_handle
from psychonaut.client import get_simple_client_session
from psychonaut.client.cursors import collect_cursored


@cli.command()
@click.argument("actor")
@as_async
async def get_followers(actor: str):
    actor = clean_handle(actor)

    async with get_simple_client_session() as sess:
        gen = collect_cursored(
            sess,
            GetFollowersReq(actor=actor, limit=100),
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
            GetFollowsResp,
            "follows"
        )

        async for follows in gen:
            print(json.dumps(follows))