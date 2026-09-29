import os
import hashlib

from cryptography.hazmat.primitives.ciphers.aead import AESGCM


ITERATIONS = 600_000
SALT_SIZE = 16
NONCE_SIZE = 12
KEY_SIZE = 32


def derive_key(password, salt):
    """
    Mengubah password menjadi AES-256 key menggunakan PBKDF2-HMAC-SHA256.
    """

    password_bytes = password.encode("utf-8")

    return hashlib.pbkdf2_hmac(
        "sha256",
        password_bytes,
        salt,
        ITERATIONS,
        KEY_SIZE
    )


def encrypt_message(message, password):
    """
    Mengenkripsi pesan menggunakan AES-GCM.

    Return:
        salt
        nonce
        ciphertext + authentication tag
    """

    salt = os.urandom(SALT_SIZE)

    key = derive_key(password, salt)

    aes = AESGCM(key)

    nonce = os.urandom(NONCE_SIZE)

    plaintext = message.encode("utf-8")

    ciphertext = aes.encrypt(
        nonce,
        plaintext,
        None
    )

    return salt, nonce, ciphertext


def decrypt_message(salt, nonce, ciphertext, password):
    """
    Mendekripsi ciphertext menggunakan password.

    Jika password salah atau data telah dimodifikasi,
    AES-GCM akan gagal melakukan autentikasi.
    """

    key = derive_key(password, salt)

    aes = AESGCM(key)

    plaintext = aes.decrypt(
        nonce,
        ciphertext,
        None
    )

    return plaintext.decode("utf-8")