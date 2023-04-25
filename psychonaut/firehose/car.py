"""


See also:

https://github.com/ipfs/go-block-format/blob/master/blocks_test.go
https://github.com/ipld/go-car/blob/164c23bc8c01a3482a8be9c75631425239fda8c6/util/util.go#L113
https://github.com/ipfs/go-cid/blob/d46e7f28669cd2c463bc68fe86e7dbe4f8240ab7/cid.go
"""
import dag_cbor
from multiformats.multihash import get
import io
import cbor2
from typing import Tuple, Union
from multiformats import CID


MAX_ALLOWED_SECTION_SIZE = 32 << 20  # 32MiB


def parse_car_blocks(blocks: bytes):
    with io.BufferedReader(io.BytesIO(blocks)) as block_fp:
        # TODO: do something with the header, i imagine.
        header = _consume_and_validate_header(block_fp)

        # Consume blocks
        blocks = []
        try:
            while True:
                # not sure on the terminology here
                node = _ld_read(block_fp)

                block = _read_block(io.BufferedReader(io.BytesIO(node)))
                blocks.append(block)
        except EOFError:
            pass

        return blocks



def _consume_and_validate_header(block_fp: io.BufferedReader):
    # Consume and validate the header.
    header_buf = _ld_read(block_fp)

    if not header_buf:
        raise EOFError("Unexpected EOF")

    header = cbor2.loads(header_buf)

    if header["version"] != 1:
        raise IOError(f"Unknown version {header.version}")

    if len(header["roots"]) == 0:
        raise ValueError("Empty car, no roots")

    return header


def _read_block(reader: io.BufferedReader, validate=True) -> CID:
    version = _read_uvarint(reader)
    if version != 1:
        raise IOError(f"Unknown version {version}")

    # https://github.com/multiformats/multihash
    # fn code  dig size hash digest
    # -------- -------- -----------------------------------
    # 00010001 00000100 10110110 11111000 01011100 10110101
    # sha1     4 bytes  4 byte sha1 digest

    block_encoding_multicodec = _read_uvarint(reader)  # skip size

    fn_code = _read_uvarint(reader)
    dig_size = int(_read_uvarint(reader))
    if dig_size > (32 << 20):  # 32MiB
        raise IOError("Multihash digest length is too long")

    hash_digest = reader.read(dig_size)

    mh = get("sha2-256")
    # TODO: use this

    data = reader.read()
    mhd = mh.digest(data)

    if validate and mhd[2:] != hash_digest:
        raise IOError(f"Multihash digest does not match: {mhd} != {hash_digest}")
    return dag_cbor.decode(data)
    #return cbor2.loads(data, tag_hook=cbor_decoder)


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




mh = dict(
    SHA2_256=0x12,
    SHA2_512=0x13,
    SHA3_224=0x17,
    SHA3_256=0x16,
    SHA3_384=0x15,
    SHA3_512=0x14,
    SHA3=0x14,
    KECCAK_224=0x1A,
    KECCAK_256=0x1B,
    KECCAK_384=0x1C,
    KECCAK_512=0x1D,
    BLAKE3=0x1E,
    SHAKE_128=0x18,
    SHAKE_256=0x19,
    BLAKE2B_MIN=0xB201,
    BLAKE2B_MAX=0xB240,
    BLAKE2S_MIN=0xB241,
    BLAKE2S_MAX=0xB260,
    MD5=0xD5,
    DBL_SHA2_256=0x56,
    MURMUR3X64_64=0x22,
    MURMUR3=0x22,
    SHA2_256_TRUNC254_PADDED=0x1012,
    X11=0x1100,
    POSEIDON_BLS12_381_A1_FC1=0xB401,
)


mh_r = {v: k for k, v in mh.items()}
