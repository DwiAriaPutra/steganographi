"""
Kapasitas steganografi sebuah gambar.

1 LSB per channel RGB, sehingga::

    capacity_bits   = width * height * 3
    capacity_bytes  = capacity_bits // 8
    max_message     = capacity_bytes - OVERHEAD
"""

from PIL import Image

from .constants import OVERHEAD


def capacity_from_size(width, height):
    """
    Menghitung kapasitas dari ukuran gambar
    tanpa membuka file.
    """

    capacity_bits = width * height * 3

    capacity_bytes = capacity_bits // 8

    max_message_bytes = max(
        capacity_bytes - OVERHEAD,
        0
    )

    return {
        "width": width,
        "height": height,
        "capacity_bits": capacity_bits,
        "capacity_bytes": capacity_bytes,
        "max_message_bytes": max_message_bytes,
    }


def get_capacity(image_path):
    """
    Menghitung kapasitas steganografi gambar.

    Returns:
        dict: width, height, capacity_bits, capacity_bytes,
            max_message_bytes.
    """

    with Image.open(image_path) as image:

        width, height = image.size

    return capacity_from_size(
        width,
        height
    )
