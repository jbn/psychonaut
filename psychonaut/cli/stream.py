from pathlib import Path
import click
import websockets
import base64
import time
from .group import cli
from .util import as_async



@cli.command()
@click.argument("output_dir", type=click.Path(exists=False), default="streams")
@as_async
async def save_base64_stream(output_dir: str):
    streams_dir = Path(output_dir)
    streams_dir.mkdir(exist_ok=True, parents=True)

    uri = "wss://bsky.social/xrpc/com.atproto.sync.subscribeRepos"
    now = int(time.time())
    out_path = streams_dir / f"stream.{now}.jsonl"
    async with websockets.connect(uri) as websocket:
        with open(out_path, "w") as fp:
            n = 0
            start = time.time()
            while True:
                msg = await websocket.recv()
                fp.write(base64.b64encode(msg).decode("utf8") + "\n")
                n += 1

                if n % 100 == 0:
                    per_second = n / (time.time() - start)
                    print(f"Received {n} messages {per_second:.2f}/s")

                # Turn msg into bytesIO
                # with io.BytesIO(msg) as fp:
                #     kind = cbor2.load(fp)
                #     obj = cbor2.load(fp)
                #     #print(kind, obj)
                #     print(kind, obj['repo'], obj.keys())

                # for blob in msg:
                #     print(cbor2.loads(blob))

                # obj = cbor2.loads(msg)
                # print(obj)
                # print(msg)
                # break