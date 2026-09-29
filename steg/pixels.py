"""
Codec pixel <-> bit LSB.

Gambar RGB dibaca menjadi list datar berisi nilai channel
seuai urutan raster::

    pixel 0: R G B | pixel 1: R G B | ...

Indeks pada list datar itulah yang dipakai ``positions``
sebagai alamat Blogs of bits.
"""

from PIL import Image


def open_rgb(image_path):
    """
    Membuka gambar dan memaksa mode RGB.

    Returns:
        PIL.Image.Image
    """

    return Image.open(image_path).convert("RGB")


def flatten(image):
    """
    Mengubah image RGB menjadi list datar nilai channel.

        list(image.tobytes())
    """

    return list(image.tobytes())


def unflatten(
    channels,
    size
):
    """
    Menyusun ulang list datar channel menjadi image RGB.
    """

    image = Image.frombytes(
        "RGB",
        size,
        bytes(channels)
    )

    return image


def write_bits(
    channels,
    positions,
    bits
):
    """
    Menulis bit pesan ke LSB channel pada posisi tertentu.

    Tidak memodifikasi list selain indeks yang dipakai.
    """

    for bit, position in zip(bits, positions):

        channels[position] = (
            channels[position] & 0b11111110
        ) | bit


def read_bits(
    channels,
    positions,
    start=0,
    count=None
):
    """
    Membaca LSB channel pada ``positions[start:count]``.

    Returns:
        list[int]: daftar bit 0/1.
    """

    end = (
        len(positions)
        if count is None
        else start + count
    )

    return [
        channels[position] & 1
        for position in positions[start:end]
    ]


def flip_lsb(
    image,
    position
):
    """
    Membalik satu bit LSB (0 <-> 1) pada ``position``.

    Dipakai untuk simulasi tampering pada pengujian.
    """

    channels = flatten(image)

    channels[position] ^= 1

    return unflatten(
        channels,
        image.size
    )
