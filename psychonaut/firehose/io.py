import base64
from contextlib import contextmanager
import json
from psychonaut.firehose.car import read_blocks, read_car

from psychonaut.firehose.serde import (
    _json_encode_kludge,
    read_first_block,
    read_msg_pair,
)
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, Tuple


@contextmanager
def noop_segment_writer():
    yield lambda msg, first_block: None


def write_length_prefixed_msg(msg: bytes, fp) -> int:
    length = len(msg)
    length_bytes = length.to_bytes(4, "big")
    fp.write(length_bytes)
    fp.write(msg)
    return 4 + length


FINALIZE_SEGMENT = Callable[(Path, int), None]


def noop_finalize_segment(path: Path, bytes_written: int):
    pass


class LengthDelimitedStreamSegmentWriter:
    def __init__(
        self,
        output_dir: Path | str,
        segment_size: int = 100_000_000,
        finalize_segment: FINALIZE_SEGMENT = noop_finalize_segment,
    ):
        self._output_dir = Path(output_dir)
        self._output_dir.mkdir(exist_ok=True, parents=True)
        self._segment_size = segment_size

        self._segment_path = None
        self._segment_fp = None
        self._bytes_written = 0
        self._finalize_segment = finalize_segment

        self._init_next_segment()

    def _init_next_segment(self):
        if self._segment_fp:
            self._segment_fp.close()
            self._finalize_segment(self._segment_path, self._bytes_written)

        now = datetime.now()
        dir_name = now.strftime("%Y-%m-%d")
        file_name = now.strftime("%H-%M-%S.length-prefixed")
        segment_dir = self._output_dir / dir_name
        if not segment_dir.exists():
            segment_dir.mkdir(exist_ok=True, parents=True)

        self._segment_path = segment_dir / file_name
        self._segment_fp = self._segment_path.open("wb")
        self._bytes_written = 0

    @property
    def segment_path(self):
        return self._segment_path

    def write(self, data: bytes):
        self._bytes_written += write_length_prefixed_msg(data, self._segment_fp)

        if self._bytes_written >= self._segment_size:
            self._init_next_segment()

    def __call__(self, msg: bytes, first_block: Dict[str, Any]):
        self.write(msg)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._segment_fp.close()


def b64line_iter(stream_path: Path):
    with stream_path.open() as f:
        for line in f:
            yield base64.b64decode(line)


def b64line_cbor2_iter(stream_path: Path):
    for msg in b64line_iter(stream_path):
        yield read_msg_pair(msg)


def length_prefixed_iter(stream_path: Path):
    # I think the limit is 1_000_000 bytes and most are much smaller than that
    # but i don't have an optimized uvarint reader yet so just do 4 bytes.
    with stream_path.open("rb") as f:
        while True:
            length_bytes = f.read(4)
            if not length_bytes:
                break
            length = int.from_bytes(length_bytes, "big")
            msg = f.read(length)
            yield msg


def convert_b64_to_length_prefixed(
    input_file: Path, output_dir: Path
) -> Tuple[Path, int]:
    n_bytes = 0

    output_name = input_file.name.replace(".b64-lines", ".length-prefixed")
    output_file = output_dir / output_name

    with output_file.open("wb") as out_fp:
        for msg in b64line_iter(input_file):
            n_bytes += write_length_prefixed_msg(msg, out_fp)

    return output_file, n_bytes


def convert_b64_to_length_prefixed_all(
    input_dir: Path, output_dir: Path, verbose=False, skip_empty=False
):
    for input_file in sorted(input_dir.glob("*.b64-lines")):
        input_mb = input_file.stat().st_size / 1_000_000
        if input_mb == 1 and not skip_empty:
            continue

        _, output_bytes = convert_b64_to_length_prefixed(input_file, output_dir)

        output_mb = output_bytes / 1_000_000
        if verbose:
            print(f"{input_file.name}: {input_mb:.2f}MB -> {output_mb:.2f}MB")


def stream_to_stdout(length_prefixed_file: Path):
    for msg in length_prefixed_iter(length_prefixed_file):
        kind, obj = read_msg_pair(msg)
        roots, blocks = read_car(obj["blocks"])
        first_block = blocks[0]

        if first_block:
            # TODO: finish pydantic models for records so no kludge needed
            try:
                obj["first_block_cid"] = first_block.cid
                obj["first_block_msg"] = first_block.decoded
                del obj["blocks"]
                line = json.dumps(_json_encode_kludge(obj))
            except TypeError:
                print(first_block)
                raise
            print(line)
