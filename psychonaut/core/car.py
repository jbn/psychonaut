from __future__ import annotations
import dag_cbor
import io
from typing import List, Tuple
from multiformats import CID
from .jit import jit

from psychonaut.core.uvarint import (
    burn_uvarint_bytes,
    read_uvarint_from_bytes,
    read_uvarint_from_bytes_no_throw,
)


MAX_ALLOWED_SECTION_SIZE = 32 << 20  # 32MiB


class ParsedBlocks:
    __slots__ = ("_header", "_blocks")

    def __init__(self, blocks: bytes, validate: bool = True):
        self._header, self._blocks = read_car(blocks, validate=validate)

    @property
    def header(self) -> bytes:
        return self._header

    @property
    def blocks(self) -> List[Block]:
        return self._blocks

    def __getitem__(self, index: int) -> Block:
        return self._blocks[index]


def read_car(blocks: bytes, validate=True) -> Tuple[List[CID], List[Block]]:
    """
    Read a car file into a list of blocks.

    From the ipld CARv1 spec:

        |--------- Header --------| |---------- Data ------------|
        [ varint | DAG-CBOR block ] [ varint | CID | block ]{1,}

    :param blocks: the car bytes
    :param validate: if True, validate the roots against the blocks
    """
    roots, offset = _get_roots(blocks, 0)
    blocks = read_blocks(blocks, offset, validate)
    return roots, blocks


class Block:
    __slots__ = ("_cid", "_data", "_decoded")

    def __init__(self, cid: CID, data: bytes):
        self._cid = cid
        self._data = data
        self._decoded = None

    @property
    def cid(self) -> CID:
        return self._cid
    
    @property
    def data(self) -> bytes:
        return self._data
    
    def __repr__(self) -> str:
        return f"Block(cid={self.cid}, data=[{len(self.data)} bytes])"

    def __eq__(self, other: Block) -> bool:
        """
        Compare blocks by CID only (assumes data was validated)
        """
        return self.cid == other.cid

    def __hash__(self) -> int:
        return hash(self.cid)

    @classmethod
    def from_bytes(cls, b: bytes, validate: bool = True) -> Block:
        cid_bytes, data = _read_cid_bytes_and_data(b, 0)
        cid = CID.decode(cid_bytes)
        if validate:
            got = cid.hashfun.digest(data) 
            if got != cid.digest:
                raise ValueError(f"CID digest does not match: {cid.digest} != {got}")
        return cls(cid=cid, data=data)

    @property
    def decoded(self) -> dag_cbor.IPLDKind:
        value = self._decoded
        if value is None:
            value = dag_cbor.decode(self.data)
            self._decoded = value
        return value


@jit(nopython=True)
def _read_cid_bytes_and_data(b: bytes, start_pos: int) -> Tuple[bytes, bytes]:
    # This borders on premature optimization. But since I
    # save a lot of firehose segments where I do validation up
    # before write and then never on read, this is useful to me.
    offset = start_pos
    for i in range(3):
        # Version, size, and hash func
        offset = burn_uvarint_bytes(b, offset)
        if offset == -1:
            raise ValueError(f"Invalid block format: uvarint loop {i}")

    # The digest size is variable
    n_digest_bytes, offset = read_uvarint_from_bytes_no_throw(b, offset)
    if n_digest_bytes == -1:
        raise ValueError("Invalid block format: digest size uvarint")

    end_pos = offset + n_digest_bytes
    if end_pos >= len(b):
        raise ValueError("Invalid block format: digest past end of data")

    return b[0:end_pos], b[end_pos:]


def read_blocks(data: bytes, offset: int, validate: bool) -> List[Block]:
    # Consume blocks
    blocks = []
    try:
        while True:
            block, offset = _ld_read_bytes(data, offset)
            blocks.append(Block.from_bytes(block, validate=validate))
    except EOFError:
        pass

    return blocks


def _get_roots(block_fp: io.BufferedReader, offset: int) -> List[CID]:
    header_buf, offset = _ld_read_bytes(block_fp, offset)
    if not header_buf:
        raise EOFError("Unexpected EOF while reading header")

    header = dag_cbor.decode(header_buf)
    if header["version"] != 1:
        raise ValueError(f"Unknown version {header.version}")

    if len(header["roots"]) == 0:
        raise ValueError("Empty car, no roots")

    return header["roots"], offset


@jit(nopython=True)
def _ld_read_bytes(b: bytes, offset: int) -> Tuple[bytes, int]:
    # See: https://github.com/ipld/go-car/blob/164c23bc8c01a3482a8be9c75631425239fda8c6/util/util.go#L113
    section_size, i = read_uvarint_from_bytes(b, offset)
    j = i + section_size
    if j > len(b):
        raise ValueError("Failed to read full buffer")

    if section_size > MAX_ALLOWED_SECTION_SIZE:  # Don't OOM
        raise ValueError(
            f"Section size {section_size} > {MAX_ALLOWED_SECTION_SIZE}"
        )

    return b[i:j], j