"""
Pengambilan pesan dari stego image (LSB).

Alur ( kebalikan dari ``steg.embed`` )::

    LSB channel pada posisi pseudorandom
       ↓
    bits → bytes
       ↓
    header (validasi magic / versi / panjang)
       ↓
    salt + nonce + ciphertext
       ↓
    AES-GCM decrypt
       ↓
    message
"""

from crypto import (
    decrypt_message,
    SALT_SIZE,
    NONCE_SIZE,
)

from .bits import bits_to_bytes

from .constants import (
    HEADER_BITS,
    GCM_TAG_SIZE,
    SALT_OFFSET,
    NONCE_OFFSET,
    CIPHERTEXT_OFFSET,
)

from .errors import PayloadError, DecryptionError

from .header import parse_header

from .pixels import (
    open_rgb,
    flatten,
    read_bits,
)

from .positions import generate_positions


def split_payload(payload):
    """
    Memisahkan payload menjadi salt, nonce, dan ciphertext.

    Raises:
        PayloadError: salah satu bagian tidak lengkap.
    """

    salt = payload[
        SALT_OFFSET:NONCE_OFFSET
    ]

    nonce = payload[
        NONCE_OFFSET:CIPHERTEXT_OFFSET
    ]

    ciphertext = payload[
        CIPHERTEXT_OFFSET:
    ]

    if len(salt) != SALT_SIZE:

        raise PayloadError("Salt tidak valid.")

    if len(nonce) != NONCE_SIZE:

        raise PayloadError("Nonce tidak valid.")

    if len(ciphertext) < GCM_TAG_SIZE:

        raise PayloadError(
            "Ciphertext tidak valid."
        )

    return salt, nonce, ciphertext


def extract_message(
    input_image,
    key
):
    """
    Mengambil pesan dari stego image.

    Returns:
        dict: message, ciphertext_bytes, payload_bytes.
    """

    image = open_rgb(input_image)

    width, height = image.size

    capacity_bits = width * height * 3

    channels = flatten(image)

    positions = generate_positions(
        capacity_bits,
        key
    )

    if capacity_bits < HEADER_BITS:

        raise PayloadError(
            "Gambar terlalu kecil untuk "
            "mengandung data steganografi."
        )

    header = bits_to_bytes(
        read_bits(
            channels,
            positions,
            0,
            HEADER_BITS
        )
    )

    payload_length = parse_header(header)

    payload_bits_required = payload_length * 8

    total_required_bits = (
        HEADER_BITS
        + payload_bits_required
    )

    if total_required_bits > capacity_bits:

        raise PayloadError(
            "Ukuran payload tidak valid."
        )

    payload = bits_to_bytes(
        read_bits(
            channels,
            positions,
            HEADER_BITS,
            payload_bits_required
        )
    )

    salt, nonce, ciphertext = split_payload(payload)

    try:

        message = decrypt_message(
            salt,
            nonce,
            ciphertext,
            key
        )

    except Exception as error:

        raise DecryptionError(
            "Pesan tidak dapat didekripsi. "
            "Stego key salah atau data rusak."
        ) from error

    return {
        "message": message,
        "ciphertext_bytes": len(ciphertext),
        "payload_bytes": len(payload),
    }
