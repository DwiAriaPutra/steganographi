"""
Uji massal: embed pesan pada beberapa cover image
lalu ukur kualitas stego image yang dihasilkan.

Jalankan::

    python test_images.py
"""

from pathlib import Path

from analysis import calculate_metrics

from steg import (
    embed_message,
    extract_message,
)


IMAGE_DIR = Path("images")

RESULT_DIR = Path("test_results")

KEY = "test-key"

MESSAGE_SIZES = [
    100,
    1000,
    4000,
]

MIN_IMAGES = 5

HEADER = "=" * 70


def generate_message(size):
    """
    Membuat pesan dummy sepanjang ``size`` byte.
    """

    return "A" * size


def test_one(
    image_path,
    message_size
):
    """
    Embed + extract pada satu gambar.

    Returns:
        dict hasil pengukuran.
    """

    message = generate_message(message_size)

    output_path = (
        RESULT_DIR
        / f"{image_path.stem}_{message_size}B.png"
    )

    embed_message(
        str(image_path),
        str(output_path),
        message,
        KEY
    )

    recovered = extract_message(
        str(output_path),
        KEY
    )["message"]

    mse, psnr = calculate_metrics(
        str(image_path),
        str(output_path)
    )

    return {
        "image": image_path.name,
        "message_size": message_size,
        "mse": mse,
        "psnr": psnr,
        "valid": recovered == message,
    }


def run_image(image_path, results):
    """
    Menjalankan semua ukuran pesan untuk satu gambar.
    """

    print()
    print("=" * 50)
    print(f"Image: {image_path.name}")
    print("=" * 50)

    for message_size in MESSAGE_SIZES:

        print()
        print(f"Testing {message_size} byte...")

        try:

            result = test_one(
                image_path,
                message_size
            )

        except ValueError as error:

            print(f"GAGAL: {error}")
            continue

        results.append(result)

        print(f"MSE   : {result['mse']}")
        print(f"PSNR  : {result['psnr']} dB")
        print(f"Valid : {result['valid']}")


def print_results(results):
    """
    Mencetak tabel rekap.
    """

    print()
    print(HEADER)
    print("HASIL AKHIR")
    print(HEADER)

    print(
        f"{'Image':<15}"
        f"{'Size (B)':<12}"
        f"{'MSE':<20}"
        f"{'PSNR (dB)':<15}"
        f"{'Valid':<8}"
    )

    print("-" * 70)

    for result in results:

        print(
            f"{result['image']:<15}"
            f"{result['message_size']:<12}"
            f"{result['mse']:<20.6f}"
            f"{result['psnr']:<15.6f}"
            f"{str(result['valid']):<8}"
        )


def main():
    """
    Entry point uji massal.
    """

    RESULT_DIR.mkdir(exist_ok=True)

    cover_images = sorted(
        IMAGE_DIR.glob("image_*.png")
    )

    if len(cover_images) < MIN_IMAGES:

        raise ValueError(
            f"Ditemukan {len(cover_images)} gambar. "
            f"Minimal {MIN_IMAGES} gambar diperlukan."
        )

    results = []

    for image_path in cover_images[:MIN_IMAGES]:

        run_image(image_path, results)

    print_results(results)


if __name__ == "__main__":

    main()
