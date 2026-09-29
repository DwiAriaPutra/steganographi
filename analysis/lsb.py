"""
Analisis LSB plane.

Black/white plane memudahkan melihat pola acak yang khas
pada LSB embedding.
"""

from PIL import Image

from steg.pixels import (
    open_rgb,
    flatten,
)


WHITE = 255
BLACK = 0


def get_lsb_plane(image_path):
    """
    Menghasilkan gambar LSB plane.

    LSB 0 -> hitam
    LSB 1 -> putih

    Pixel disorot putih bila minimal satu channel
    memiliki LSB bernilai 1.
    """

    image = open_rgb(image_path)

    channels = flatten(image)

    pixels = [
        WHITE if (
            channels[i] & 1
            or channels[i + 1] & 1
            or channels[i + 2] & 1
        ) else BLACK
        for i in range(
            0,
            len(channels),
            3
        )
    ]

    return build_plane(
        pixels,
        image.size
    )


def get_lsb_difference(
    cover_image,
    stego_image
):
    """
    Membandingkan LSB cover dan stego.

    Hitam:
        tidak ada LSB channel yang berubah.
    Putih:
        minimal satu channel berubah LSB-nya.
    """

    cover = open_rgb(cover_image)

    stego = open_rgb(stego_image)

    if cover.size != stego.size:

        raise ValueError(
            "Ukuran gambar berbeda."
        )

    cover_channels = flatten(cover)

    stego_channels = flatten(stego)

    pixels = [
        WHITE if (
            cover_channels[i] & 1
            != stego_channels[i] & 1
            or cover_channels[i + 1] & 1
            != stego_channels[i + 1] & 1
            or cover_channels[i + 2] & 1
            != stego_channels[i + 2] & 1
        ) else BLACK
        for i in range(
            0,
            len(cover_channels),
            3
        )
    ]

    return build_plane(
        pixels,
        cover.size
    )


def build_plane(pixels, size):
    """
    Menyusun list nilai 0/255 menjadi image mode "L".
    """

    result = Image.new(
        "L",
        size
    )

    result.putdata(pixels)

    return result
