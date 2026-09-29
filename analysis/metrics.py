"""
Metrik kualitas gambar antara cover image dan stego image.

Perhitungan memakai channel datar (lihat ``steg.pixels.flatten``)
sehingga MSE dan PSNR identik dengan definisi standar
atas seluruh komponen R, G, dan B.
"""

import math

from steg.pixels import (
    open_rgb,
    flatten,
)


MAX_PIXEL_VALUE = 255


def calculate_metrics(
    cover_image,
    stego_image
):
    """
    Menghitung MSE dan PSNR antara dua gambar.

    Returns:
        tuple[float, float]: (mse, psnr dalam dB).
            psnr = float("inf") jika kedua gambar identik.

    Raises:
        ValueError: ukuran kedua gambar berbeda.
    """

    cover = open_rgb(cover_image)

    stego = open_rgb(stego_image)

    if cover.size != stego.size:

        raise ValueError(
            "Ukuran gambar berbeda."
        )

    cover_channels = flatten(cover)

    stego_channels = flatten(stego)

    total_squared_error = 0

    for cover_value, stego_value in zip(
        cover_channels,
        stego_channels
    ):

        difference = (
            cover_value - stego_value
        )

        total_squared_error += (
            difference * difference
        )

    mse = total_squared_error / len(
        cover_channels
    )

    psnr = calculate_psnr(mse)

    return mse, psnr


def calculate_psnr(mse):
    """
    Mengubah MSE menjadi PSNR (dB).
    """

    if mse == 0:

        return float("inf")

    return 10 * math.log10(
        (MAX_PIXEL_VALUE ** 2) / mse
    )
