"""
Pembuatan urutan posisi pixel/channel yang pseudorandom.

Posisi dihitung dari ``stego key`` sehingga cover dan stego image
menggunakan urutan yang sama, tanpa perlu menyimpan posisi
di dalam gambar.
"""

import random


def generate_positions(capacity, key):
    """
    Membuat urutan posisi pixel/channel berdasarkan stego key.

    Contoh:
        capacity = 10

    posisi awal:
        0 1 2 3 4 5 6 7 8 9

    setelah shuffle:
        4 8 1 9 0 3 7 2 6 5

    Selama key dan capacity sama,
    urutan yang dihasilkan juga sama.
    """

    positions = list(
        range(capacity)
    )

    random.Random(key).shuffle(positions)

    return positions
