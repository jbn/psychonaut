import json
from typing import Tuple
import click

from psychonaut.cli.util import clean_handle
from .group import cli
from .util import as_async, print_error_and_fail
from psychonaut.api.lexicons.app.bsky.actor.get_profiles import (
    GetProfilesReq,
    get_profiles as get_profiles_f,
)
from psychonaut.api.lexicons.app.bsky.actor.get_profile import (
    GetProfileReq,
    get_profile as get_profile_f,
)
from psychonaut.api.lexicons.com.atproto.identity.resolve_handle import (
    ResolveHandleReq,
    resolve_handle as resolve_handle_f,
)
from psychonaut.client import get_simple_client_session


@cli.command()
@click.argument("handle")
@as_async
async def resolve_handle(handle: str):
    handle = clean_handle(handle)
    
    if not handle:
        print_error_and_fail("No handle provided")

    async with get_simple_client_session() as sess:
        req = ResolveHandleReq(handle=handle)
        resp = await resolve_handle_f(sess, req)
        print(resp.json())


@cli.command()
@click.argument("actors", nargs=-1)
@as_async
async def get_profiles(actors: Tuple[str]):
    actors = [
        clean_handle(actor)
        for actor in actors
        if clean_handle(actor)
    ]

    if not actors:
        print_error_and_fail("No actors provided")

    async with get_simple_client_session() as sess:
        req = GetProfilesReq(actors=actors)
        resp = await get_profiles_f(sess, req)
        for profile in resp.profiles:
            print(json.dumps(profile))



@cli.command()
@click.argument('actor', nargs=1)
@as_async
async def get_profile(actor: str):
    actor = clean_handle(actor)
    if not actor:
        print_error_and_fail("No actor provided")

    async with get_simple_client_session() as sess:
        req = GetProfileReq(actor=actor)
        resp = await get_profile_f(sess, req)
        print(json.dumps(resp))


