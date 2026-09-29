"""
Implementasi aksi CLI (embed / extract / capacity).

Setiap aksi mengembalikan None bila gagal: pesan error
sudah dicetak sehingga alur menu tetap aman.
"""

from steg import (
    embed_message,
    extract_message,
    get_capacity,
)

from .prompts import ask, ask_path, heading


def print_capacity():
    """
    Menampilkan informasi kapasitas sebuah gambar.
    """

    image_path = ask_path("Path gambar: ")

    try:

        info = get_capacity(image_path)

    except Exception as error:

        print(f"Error: {error}")
        return

    heading("Informasi gambar")

    print(
        f"Ukuran       : "
        f"{info['width']} x {info['height']}"
    )

    print(
        f"Kapasitas bit: "
        f"{info['capacity_bits']}"
    )

    print(
        f"Kapasitas raw: "
        f"{info['capacity_bytes']} byte"
    )

    print(
        f"Maks pesan   : "
        f"{info['max_message_bytes']} byte"
    )


def embed():
    """
    Menu embed message.
    """

    input_image = ask("Cover image: ")

    output_image = ask("Output image: ")

    message = ask("Pesan: ", strip=False)

    key = ask("Stego key: ", strip=False)

    try:

        result = embed_message(
            input_image,
            output_image,
            message,
            key
        )

    except Exception as error:

        print(f"Error: {error}")
        return

    print()
    print("Embed berhasil.")

    print(
        f"Pesan       : "
        f"{result['message_bytes']} byte"
    )

    print(
        f"Output      : "
        f"{result['output_image']}"
    )


def extract():
    """
    Menu extract message.
    """

    image = ask("Stego image: ")

    key = ask("Stego key: ", strip=False)

    try:

        result = extract_message(image, key)

    except Exception as error:

        print(f"Error: {error}")
        return

    print()
    print("Extract berhasil.")
    print()
    print("Pesan:")
    print(result["message"])


ACTIONS = {
    "1": embed,
    "2": extract,
    "3": print_capacity,
}
