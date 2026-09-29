"""
Konversi antara bytes dan list bit.

Urutan bit = MSB first, sehingga bytes -> bits -> bytes
adalah lossless.
"""

from .errors import StegoError


def bytes_to_bits(data):
    """
    Mengubah bytes menjadi list berisi bit 0/1.

    Contoh:
        b"\\xff" -> [1, 1, 1, 1, 1, 1, 1, 1]
    """

    bits = []

    for byte in data:

        for shift in range(7, -1, -1):

            bits.append(
                (byte >> shift) & 1
            )

    return bits


def bits_to_bytes(bits):
    """
    Mengubah list bit menjadi bytes.

    Raises:
        StegoError: jika jumlah bit bukan kelipatan 8.
    """

    if len(bits) % 8 != 0:

        raise StegoError(
            "Jumlah bit bukan kelipatan 8."
        )

    result = bytearray()

    for i in range(0, len(bits), 8):

        byte = 0

        for bit in bits[i:i + 8]:

            byte = (byte << 1) | bit

        result.append(byte)

    return bytes(result)
