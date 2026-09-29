"""
Core steganografi: LSB embedding + AES-GCM.

Penggunaan::

    from steg import embed_message, extract_message, get_capacity

Modul ini sengaja tidak menyentuh GUI maupun CLI, sehingga
dapat dipakai ulang di skrip uji, batch job, atau service.
"""

from .bits import (
    bytes_to_bits,
    bits_to_bytes,
)

from .capacity import (
    get_capacity,
    capacity_from_size,
)

from .constants import (
    MAGIC,
    VERSION,
    HEADER_SIZE,
    HEADER_BITS,
    GCM_TAG_SIZE,
    OVERHEAD,
    SALT_OFFSET,
    NONCE_OFFSET,
    CIPHERTEXT_OFFSET,
)

from .embed import embed_message

from .errors import (
    StegoError,
    CapacityError,
    HeaderError,
    PayloadError,
    DecryptionError,
)

from .extract import extract_message

from .header import (
    create_header,
    parse_header,
)

from .pixels import (
    open_rgb,
    flatten,
    unflatten,
    read_bits,
    write_bits,
    flip_lsb,
)

from .positions import generate_positions


__all__ = [
    "embed_message",
    "extract_message",
    "get_capacity",
    "capacity_from_size",
    "bytes_to_bits",
    "bits_to_bytes",
    "create_header",
    "parse_header",
    "generate_positions",
    "open_rgb",
    "flatten",
    "unflatten",
    "read_bits",
    "write_bits",
    "flip_lsb",
    "StegoError",
    "CapacityError",
    "HeaderError",
    "PayloadError",
    "DecryptionError",
    "MAGIC",
    "VERSION",
    "HEADER_SIZE",
    "HEADER_BITS",
    "GCM_TAG_SIZE",
    "OVERHEAD",
    "SALT_OFFSET",
    "NONCE_OFFSET",
    "CIPHERTEXT_OFFSET",
]
