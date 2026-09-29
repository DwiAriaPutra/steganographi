"""
Konstanta format data steganografi (versi 1).

Data yang ditanam di gambar::

    data = HEADER + PAYLOAD

    HEADER  = MAGIC (4B) | VERSION (1B) | LENGTH (4B)   -> 9 byte
    PAYLOAD = SALT (16B) | NONCE (12B) | CIPHERTEXT (+ GCM tag 16B)

``LENGTH`` menyimpan panjang PAYLOAD dalam byte, bukan panjang
plaintext. Semua konstanta ukuran kriptografi diambil dari
``crypto`` supaya tidak ada duplikasi angka.
"""

from crypto import SALT_SIZE, NONCE_SIZE


MAGIC = b"STG1"
VERSION = 1

HEADER_SIZE = 9
HEADER_BITS = HEADER_SIZE * 8

GCM_TAG_SIZE = 16

OVERHEAD = (
    HEADER_SIZE
    + SALT_SIZE
    + NONCE_SIZE
    + GCM_TAG_SIZE
)

SALT_OFFSET = 0
NONCE_OFFSET = SALT_OFFSET + SALT_SIZE
CIPHERTEXT_OFFSET = NONCE_OFFSET + NONCE_SIZE
