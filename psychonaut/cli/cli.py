from datetime import datetime
import json
import os
from pathlib import Path
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

@cli.command()
@click.argument("handle")
@click.option("--allow-overwrite", is_flag=True, default=False)
def save_login(handle: str, allow_overwrite: bool):
    file_path = Path().home() / ".psychonaut.json"

    if file_path.exists() and not allow_overwrite:
        print(f"File {file_path} exists, use --allow-overwrite to overwrite")
        sys.exit(1)

    # read the password
    password = click.prompt(f"Enter password for {handle}", hide_input=True)

    # write the file
    file_path.write_text(
        json.dumps(
            {
                "username": handle,
                "password": password,
            }
        )
    )


# TODO: test poetry install
if __name__ == "__main__":
    cli()
