"""
Pembulatan angka untuk label tick sumbu.

Fungsi murni tanpa Tk, dipakai ``gui.chart`` supaya
tick selalu "bulat" (1 / 2 / 2.5 / 5 x 10^n) pada
segala level zoom.
"""

import math


NICE_STEPS = (1, 2, 2.5, 5, 10)

TARGET_Y_TICKS = 5

SUFFIX = ("k", "M")


def nice_ceiling(value):
    """
    Membulatkan nilai ke atas menjadi angka "bulat"
    (1 / 2 / 2.5 / 5 × 10ⁿ) supaya label sumbu enak dibaca.

    Contoh:
        4_823  -> 5_000
        12_400 -> 20_000
    """

    if value <= 0:

        return 1

    exponent = math.floor(
        math.log10(value)
    )

    base = 10 ** exponent

    fraction = value / base

    for step in NICE_STEPS:

        if fraction <= step + 1e-9:

            return step * base

    return 10 * base


def nice_step(span, count=TARGET_Y_TICKS):
    """
    Menentukan jarak tick yang rapi untuk rentang tertentu.
    """

    if span <= 0:

        return 1

    raw = span / max(count, 1)

    return nice_ceiling(raw)


def format_tick(value):
    """
    Format angka untuk label sumbu Y.
    """

    if abs(value) >= 1_000_000:

        return f"{value / 1_000_000:.1f}M"

    if abs(value) >= 1_000:

        return f"{value / 1_000:.6g}k"

    if float(value).is_integer():

        return f"{int(value)}"

    return f"{value:.6g}"
