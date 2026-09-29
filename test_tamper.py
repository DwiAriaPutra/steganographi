"""
Uji tamper: flipping satu bit LSB pada ciphertext
harus membuat ekstraksi gagal (AES-GCM auth tag).

Jalankan setelah ``test_images.py``::

    python test_tamper.py
"""

from steg import (
    CIPHERTEXT_OFFSET,
    HEADER_BITS,
    DecryptionError,
    extract_message,
    generate_positions,
)

from steg.pixels import (
    open_rgb,
    flip_lsb,
)


INPUT_IMAGE = "test_results/image_1_4000B.png"

OUTPUT_IMAGE = "test_results/image_1_4000B_tampered.png"

KEY = "test-key"


def flip_first_ciphertext_bit():
    """
    Membalik LSB pada bit pertama ciphertext.

    Returns:
        tuple: (pixel_index, channel_index)
    """

    image = open_rgb(INPUT_IMAGE)

    width, height = image.size

    capacity_bits = width * height * 3

    positions = generate_positions(
        capacity_bits,
        KEY
    )

    bit_index = (
        HEADER_BITS
        + CIPHERTEXT_OFFSET * 8
    )

    position = positions[bit_index]

    tampered = flip_lsb(
        image,
        position
    )

    tampered.save(OUTPUT_IMAGE)

    return position // 3, position % 3


def main():
    """
    Menjalankan skenario tamper.
    """

    pixel_index, channel_index = (
        flip_first_ciphertext_bit()
    )

    print("Tampering berhasil dilakukan.")
    print("Output      :", OUTPUT_IMAGE)
    print("Pixel index :", pixel_index)
    print("Channel     :", channel_index)

    try:

        extract_message(OUTPUT_IMAGE, KEY)

    except DecryptionError as error:

        print("Deteksi tamper berhasil:", error)
        return

    print("GAGAL: pesan masih bisa diekstrak.")


if __name__ == "__main__":

    main()
