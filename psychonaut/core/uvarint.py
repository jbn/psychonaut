import io
from typing import Tuple
from .jit import jit


def read_uvarint_from_reader(reader: io.BufferedReader) -> int:
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


@jit(nopython=True)
def read_uvarint_from_bytes(data: bytes, offset: int = 0) -> Tuple[int, int]:
    result, offset = read_uvarint_from_bytes_no_throw(data, offset)
    if result == -1:
        raise EOFError("Unexpected EOF while reading uvarint")
    return result, offset


@jit(nopython=True, inline='always')
def read_uvarint_from_bytes_no_throw(data: bytes, offset: int = 0) -> Tuple[int, int]:
    # TODO: guard against BigInt?
    shift = 0
    result = 0
    while True:
        if offset >= len(data):
            return -1, offset

        byte = data[offset]
        result |= (byte & 0x7F) << shift
        offset += 1  

        if byte & 0x80 == 0:
            break
        shift += 7

    return result, offset


@jit(nopython=True, inline='always')
def burn_uvarint_bytes(data: bytes, offset: int = 0) -> int:
    while True:
        if offset >= len(data):
            return -1

        byte = data[offset]
        offset += 1

        if byte & 0x80 == 0:
            break

    return offset

