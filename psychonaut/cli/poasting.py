
from typing import Tuple
import click
from psychonaut.cli.group import cli
from psychonaut.cli.util import as_async
from psychonaut.client import get_simple_client_session
from psychonaut.api.lexicons.app.bsky.feed.post import PostReq, post
# from psychonaut.api.lexicons.com.atproto.repo.upload_blob import (
#     UploadBlobReq,
#     upload_blob as upload_blob_f,
#     UploadBlobResp,
# )
from datetime import datetime
from pathlib import Path


@cli.command()
@click.argument("text")
@click.option("--image", "-i", multiple=True)
@as_async
async def poast(text: str, image: Tuple[str]):
    if image:
        # Verify each one exists
        for path in image:
            if not Path(path).exists():
                print(f"Image {path} does not exist")
                return

    async with get_simple_client_session() as sess:
        req = PostReq(text=text, createdAt=datetime.utcnow().isoformat())

        if image:
            images = []
            for img in image:
                content_type = "image/jpeg"  # TODO: get content type robustly
                if img.endswith(".png"):
                    content_type = "image/png"
                elif img.endswith(".gif"):
                    content_type = "image/gif"
                elif img.endswith(".webp"):
                    content_type = "image/webp"

                with open(img, "rb") as f:
                    img_bytes = f.read()

                resp = (await sess._post_blob_kludge(img_bytes, content_type))['blob']
                images.append(resp)

            embed = {
                "$type": "app.bsky.embed.images",
                "images": [
                    {
                        "alt": "",  # TODO: get alt text
                        "image": img
                    }
                    for img in images
                ]
            }
            req = req.copy(update={"embed": embed})

        resp = await post(sess, req)
        print(resp)


