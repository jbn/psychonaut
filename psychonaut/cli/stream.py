import json
from pathlib import Path
import sys
import click
import websockets
import base64
import time

from psychonaut.firehose.serde import (
    read_first_block,
    stream_to_stdout,
    _json_encode_kludge,
)
from .group import cli
from .util import as_async, print_error_and_fail
import asyncio


@cli.command()
@click.argument("output_dir", type=click.Path(exists=False))
@click.option("--tee", is_flag=True, help="Write to stdout as well as file")
@as_async
async def repos_firehose_stream(output_dir: str, tee: bool):
    try:
        await _stream_run(output_dir, tee)
    except KeyboardInterrupt:
        raise
    except Exception as e:
        # Sleep for 10 seconds and continue
        print(f"Error: {e}", file=sys.stderr)
        await asyncio.sleep(10)


async def _stream_run(output_dir: str, tee: bool):
    callbacks = []
    if tee:

        def stdout_callback(msg, first_block):
            if first_block:
                print(json.dumps(_json_encode_kludge(first_block)))

        callbacks.append(stdout_callback)

    if output_dir:
        streams_dir = Path(output_dir)
        streams_dir.mkdir(exist_ok=True, parents=True)

        now = int(time.time())
        out_path = streams_dir / f"stream.{now}.b64-lines"
        out_fp = out_path.open("w")

        def file_callback(msg, first_block):
            out_fp.write(base64.b64encode(msg).decode("utf8") + "\n")

        callbacks.append(file_callback)

    if not tee and not output_dir:
        print_error_and_fail("Must specify either --tee or --output-dir")

    uri = "wss://bsky.social/xrpc/com.atproto.sync.subscribeRepos"
    async with websockets.connect(uri) as websocket:
        with open(out_path, "w") as fp:
            n = 0
            start = time.time()
            while True:
                # Read the websocket message.
                msg = await websocket.recv()

                # Read the first block.
                #
                # Why the first block? intuition alone. i assume that's a property of
                # the MST or something, which i have not learned yet. so i guess
                # assume i am wrong for now.
                first_block = read_first_block(msg)

                for f in callbacks:
                    f(msg, first_block)

                if not tee and n % 100 == 0:
                    per_second = n / (time.time() - start)
                    print(f"Received {n} messages {per_second:.2f}/s")

                n += 1


@cli.command
@click.argument("b64line_file", type=click.Path(exists=False))
def repos_firehose_replay(b64line_file: str):
    b64line_file = Path(b64line_file)
    if not b64line_file.exists():
        print_error_and_fail(f"File {b64line_file} does not exist")

    if b64line_file.is_file():
        stream_to_stdout(b64line_file)

    elif b64line_file.is_dir():
        for p in sorted(b64line_file.glob("*.b64-lines")):
            stream_to_stdout(p)
