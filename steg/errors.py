"""
Exception hierarchy untuk core steganografi.

Semua error mewarisi ``ValueError`` agar pemanggil lama
(``except ValueError``) tetap bekerja.
"""


class StegoError(ValueError):
    """
    Error dasar untuk semua kegagalan steganografi.
    """


class CapacityError(StegoError):
    """
    Pesan tidak muat pada cover image.
    """


class HeaderError(StegoError):
    """
    Header tidak ditemukan / tidak valid.
    """


class PayloadError(StegoError):
    """
    Ukuran atau isi payload tidak valid.
    """


class DecryptionError(StegoError):
    """
    Payload tidak bisa didekripsi (key salah / data rusak).
    """
