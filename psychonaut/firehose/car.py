"""


See also:

https://github.com/ipfs/go-block-format/blob/master/blocks_test.go
https://github.com/ipld/go-car/blob/164c23bc8c01a3482a8be9c75631425239fda8c6/util/util.go#L113
https://github.com/ipfs/go-cid/blob/d46e7f28669cd2c463bc68fe86e7dbe4f8240ab7/cid.go

or,

atproto/repo/src/utils.ts
"""
from __future__ import annotations
import dag_cbor
from multiformats.multihash import get
import io
from typing import List, Tuple, Union
from multiformats import CID
from pydantic import BaseModel, validator


MAX_ALLOWED_SECTION_SIZE = 32 << 20  # 32MiB



def read_car(blocks: bytes, validate=True) -> Tuple[List[CID], List[Block]]:
    """
    Read a car file into a list of blocks.

    :param blocks: the car bytes
    :param validate: if True, validate the roots against the blocks
    """
    with io.BufferedReader(io.BytesIO(blocks)) as block_fp:
        roots = _get_roots(block_fp)
        blocks = read_blocks(block_fp)
        return roots, blocks



class Block(BaseModel):
    cid: CID
    data: bytes

    @validator("cid", pre=True)
    def validate_cid(cls, value):
        if isinstance(value, CID):
            return value
        try:
            return CID(value)
        except ValueError as e:
            raise ValueError(f"Invalid CID: {e}")

    @classmethod
    def from_bytes(cls, b: bytes, validate: bool = True) -> Block:
        reader: io.BufferedReader = io.BufferedReader(io.BytesIO(b))

        start_pos = reader.tell()

        version = _read_uvarint(reader)
        if version != 1:
            raise IOError(f"Unknown version {version}")

        # TODO: This is very obviously bad. It's 2x operations.
        # I figured this part out first, then figured out the CID
        # part. It works now but it's bad.
        _read_uvarint(reader)  # skip size
        _read_uvarint(reader)
        dig_size = int(_read_uvarint(reader))
        if dig_size > (32 << 20):  # 32MiB
            raise IOError("Multihash digest length is too long")
        reader.read(dig_size)
        end_pos = reader.tell()

        data = reader.read()

        cid = CID.decode(b[start_pos:end_pos])
        if validate and cid.hashfun.digest(data) != cid.digest:
            raise ValueError("CID digest does not match")

        return cls(cid=cid, data=data)

    @property
    def decoded(self):
        return dag_cbor.decode(self.data)

    class Config:
        arbitrary_types_allowed = True


def read_blocks(block_fp: io.BufferedReader) -> List[Block]:
    # Consume blocks
    blocks = []
    try:
        while True:
            blocks.append(Block.from_bytes(_ld_read(block_fp)))
    except EOFError:
        pass

    return blocks


def _get_roots(block_fp: io.BufferedReader) -> List[CID]:
    header_buf = _ld_read(block_fp)
    if not header_buf:
        raise EOFError("Unexpected EOF")

    header = dag_cbor.decode(header_buf)
    if header["version"] != 1:
        raise IOError(f"Unknown version {header.version}")

    if len(header["roots"]) == 0:
        raise ValueError("Empty car, no roots")

    return header["roots"]


def _read_uvarint(reader: io.BufferedReader) -> int:
    # TODO: find a python uvarint implementation (this is gonna be slow as shit)
    shift = 0
    result = 0
    while True:
        b = reader.read(1)
        if not b:
            raise EOFError("Unexpected EOF")

        byte = b[0]
        result |= (byte & 0x7F) << shift
        if byte & 0x80 == 0:
            break
        shift += 7

    return result


def _ld_read(
    reader: io.BufferedReader,
) -> Tuple[Union[bytes, None], Union[None, IOError]]:
    peek = reader.peek(1)

    if not peek:
        raise EOFError("Unexpected EOF")

    buf_size = _read_uvarint(reader)

    if buf_size > MAX_ALLOWED_SECTION_SIZE:  # Don't OOM
        raise IOError(
            f"Malformed car; header is bigger than {MAX_ALLOWED_SECTION_SIZE}"
        )

    buf = reader.read(buf_size)
    if len(buf) != buf_size:
        raise IOError("Failed to read full buffer")

    return buf
