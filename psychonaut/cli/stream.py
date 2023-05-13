import json
from pathlib import Path
import sys
import click
import websockets
import time
from psychonaut.firehose.exponential_backoff import FirehoseExponentialBackoff
from psychonaut.firehose.io import (
    LengthDelimitedStreamSegmentWriter,
    convert_b64_to_length_prefixed_all,
    iter_length_prefixed_paths,
    noop_segment_writer,
    stream_to_stdout,
)

from psychonaut.firehose.serde import (
    read_jsonified_event,
    _json_encode_kludge,
)
from .group import cli
from .util import as_async, print_error_and_fail
import asyncio


@cli.command()
@click.argument("output_dir", type=click.Path(exists=False))
@click.option("--tee", is_flag=True, help="Write to stdout as well as file")
@click.option("--tee-first-block-only", is_flag=True, help="Only print the first block")
@as_async
async def repos_firehose_stream(output_dir: str, tee: bool, tee_first_block_only: bool):
    segment_writer = noop_segment_writer()

    if output_dir:
        segment_writer = LengthDelimitedStreamSegmentWriter(
            output_dir,
            finalize_segment=lambda path, bytes_written: print(
                f"Wrote {bytes_written} bytes to {path}"
            ),
        )

    backoff = FirehoseExponentialBackoff()

    with segment_writer as writer:
        while True:
            try:
                await _stream_run(
                    output_dir, tee, writer, tee_first_block_only
                )  # TODO: clean up
                backoff.reset()
            except KeyboardInterrupt:
                raise
            except Exception as e:
                raise e
                sleep_time = backoff.next_sleep_time()
                print(f"Error: {e}", file=sys.stderr)
                print(f"\tSleeping for {sleep_time} seconds", file=sys.stderr)
                await asyncio.sleep(sleep_time)


def _has_one_block(jsonified_event):
    return "blocks" in jsonified_event and len(jsonified_event["blocks"]) > 0


async def _stream_run(
    output_dir: str, tee: bool, writer, tee_first_block_only: bool = False
):
    callbacks = []
    if tee:

        def stdout_callback(msg, jsonified_event):
            if jsonified_event:
                if tee_first_block_only and _has_one_block(jsonified_event):
                    jsonified_event["blocks"] = [jsonified_event["blocks"][0]]
                    jsonified_event["block_cids"] = [jsonified_event["block_cids"][0]]
                print(json.dumps(_json_encode_kludge(jsonified_event)))

        callbacks.append(stdout_callback)

    if output_dir:
        callbacks.append(writer)

    if not tee and not output_dir:
        print_error_and_fail("Must specify either --tee or --output-dir")

    uri = "wss://bsky.social/xrpc/com.atproto.sync.subscribeRepos"
    async with websockets.connect(uri) as websocket:
        n = 0
        start = time.time()
        while True:
            # Read the websocket message.
            msg = await websocket.recv()

            # msg = await asyncio.wait_for(websocket.recv(), timeout=1)

            # Read the first block.
            #

            # TODO: clean this up its kinda just a mess & bandaid
            jsonified_event = read_jsonified_event(msg)

            for f in callbacks:
                f(msg, jsonified_event)

            if not tee and n % 100 == 0:
                per_second = n / (time.time() - start)
                print(f"Received {n} messages {per_second:.2f}/s")

            n += 1


@cli.command
@click.argument("length_prefixed_file", type=click.Path(exists=False))
def repos_firehose_replay(length_prefixed_file: str):
    length_prefixed_file = Path(length_prefixed_file)
    if not length_prefixed_file.exists():
        print_error_and_fail(f"File {length_prefixed_file} does not exist")

    if length_prefixed_file.is_file():
        stream_to_stdout(length_prefixed_file)

    elif length_prefixed_file.is_dir():
        for p in iter_length_prefixed_paths(length_prefixed_file):
            stream_to_stdout(p)


@cli.command()
@click.argument("input_dir", type=click.Path(exists=True))
@click.argument("output_dir", type=click.Path(exists=False))
@click.option("--verbose", is_flag=True, help="Print progress")
@click.option("--skip-empty", is_flag=True, help="Skip files with 0 bytes")
def b64_dir_to_length_prefixed(
    input_dir: str, output_dir: str, verbose: bool, skip_empty: bool
):
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    convert_b64_to_length_prefixed_all(input_dir, output_dir, verbose)
