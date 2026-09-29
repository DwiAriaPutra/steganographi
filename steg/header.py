"""
Baca / tulis header format steganografi.

Header 9 byte::

    MAGIC (4B) | VERSION (1B) | LENGTH (4B, big endian)
"""

import struct

from .constants import (
    MAGIC,
    VERSION,
    HEADER_SIZE,
)

from .errors import HeaderError


def create_header(payload_length):
    """
    Membuat header dari panjang payload (byte).
    """

    return (
        MAGIC
        + bytes([VERSION])
        + struct.pack(">I", payload_length)
    )


def parse_header(header):
    """
    Memvalidasi header dan mengembalikan panjang payload.

    Raises:
        HeaderError: panjang salah, magic salah, atau versi
            tidak didukung.
    """

    if len(header) != HEADER_SIZE:

        raise HeaderError(
            "Header tidak valid."
        )

    if header[:4] != MAGIC:

        raise HeaderError(
            "Data steganografi tidak ditemukan "
            "atau stego key salah."
        )

    version = header[4]

    if version != VERSION:

        raise HeaderError(
            "Versi data steganografi tidak didukung."
        )

    return struct.unpack(
        ">I",
        header[5:HEADER_SIZE]
    )[0]
