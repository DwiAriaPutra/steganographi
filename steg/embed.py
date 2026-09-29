"""
Penyisipan pesan terenkripsi ke dalam gambar (LSB).

Alur::

    message
       ↓
    AES-GCM  (crypto.encrypt_message)
       ↓
    header + salt + nonce + ciphertext
       ↓
    bytes → bits
       ↓
    LSB channel pada posisi pseudorandom
       ↓
    stego image
"""

from crypto import encrypt_message

from .bits import bytes_to_bits

from .constants import OVERHEAD

from .errors import CapacityError

from .header import create_header

from .pixels import (
    open_rgb,
    flatten,
    unflatten,
    write_bits,
)

from .positions import generate_positions


def ensure_fits(
    total_bits,
    capacity_bits
):
    """
    Memastikan data muat pada gambar.

    Raises:
        CapacityError: data lebih besar dari kapasitas.
    """

    if total_bits <= capacity_bits:

        return

    max_message = (
        capacity_bits // 8
        - OVERHEAD
    )

    raise CapacityError(
        f"Pesan terlalu besar.\n"
        f"Maksimal pesan: {max_message} byte"
    )


def output_format(output_image):
    """
    Menentukan format simpan dari ekstensi output.

    Default PNG supaya payload tidak terpotong oleh
    kompresi lossy.
    """

    lowered = output_image.lower()

    for extension, image_format in (
        (".bmp", "BMP"),
        (".png", "PNG"),
    ):

        if lowered.endswith(extension):

            return image_format

    return "PNG"


def embed_message(
    input_image,
    output_image,
    message,
    key
):
    """
    Menyisipkan pesan terenkripsi ke dalam gambar.

    Args:
        input_image: path cover image.
        output_image: path stego image hasil.
        message: pesan plaintext.
        key: stego key (password + seed posisi pixel).

    Returns:
        dict: width, height, message_bytes, payload_bytes,
            total_bytes, output_image.
    """

    image = open_rgb(input_image)

    width, height = image.size

    capacity_bits = width * height * 3

    salt, nonce, ciphertext = encrypt_message(
        message,
        key
    )

    payload = salt + nonce + ciphertext

    data = create_header(len(payload)) + payload

    bits = bytes_to_bits(data)

    ensure_fits(
        len(bits),
        capacity_bits
    )

    positions = generate_positions(
        capacity_bits,
        key
    )

    channels = flatten(image)

    write_bits(
        channels,
        positions,
        bits
    )

    stego_image = unflatten(
        channels,
        (width, height)
    )

    stego_image.save(
        output_image,
        format=output_format(output_image)
    )

    return {
        "width": width,
        "height": height,
        "message_bytes": len(
            message.encode("utf-8")
        ),
        "payload_bytes": len(payload),
        "total_bytes": len(data),
        "output_image": output_image,
    }
