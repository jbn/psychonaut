from datetime import datetime
import os
import sys
from typing import List
import click
import asyncio
from functools import wraps
from psychonaut.api.lexicons.app.bsky.actor.get_profiles import (
    GetProfilesReq,
    get_profiles as get_profiles_f,
)
from psychonaut.api.lexicons.com.atproto.identity.resolve_handle import (
    ResolveHandleReq,
    resolve_handle as resolve_handle_f,
)
from psychonaut.client import get_simple_client_session
from psychonaut.api.lexicons.app.bsky.feed.post import PostReq, post


def as_async(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return asyncio.run(func(*args, **kwargs))

    return wrapper


@click.group()
def cli():
    pass


@cli.command()
@click.argument("text")
@as_async
async def poast(text: str):
    async with get_simple_client_session() as sess:
        req = PostReq(text=text, createdAt=datetime.utcnow().isoformat())
        resp = await post(sess, req)
        print(resp)


@cli.command()
@click.argument("handle")
@as_async
async def resolve_handle(handle: str):
    async with get_simple_client_session() as sess:
        req = ResolveHandleReq(handle=handle)
        resp = await resolve_handle_f(sess, req)
        print(resp.json())


@cli.command()
@click.argument("actors", nargs=-1)
@as_async
async def get_profiles(actors: List[str]):
    if not actors:
        print("No actors provided", file=sys.stderr)
        sys.exit(1)

    async with get_simple_client_session() as sess:
        req = GetProfilesReq(actors=actors)
        resp = await get_profiles_f(sess, req)
        for profile in resp.profiles:
            print(resp.json())


# TODO: test poetry install
if __name__ == "__main__":
    cli()
