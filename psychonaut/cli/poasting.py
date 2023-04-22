
import click
from psychonaut.cli.group import cli
from psychonaut.cli.util import as_async
from psychonaut.client import get_simple_client_session
from psychonaut.api.lexicons.app.bsky.feed.post import PostReq, post
from datetime import datetime


@cli.command()
@click.argument("text")
@as_async
async def poast(text: str):
    async with get_simple_client_session() as sess:
        req = PostReq(text=text, createdAt=datetime.utcnow().isoformat())
        resp = await post(sess, req)
        print(resp)


