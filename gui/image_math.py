"""
Perhitungan geometri penampil gambar.

Pisahkan dari Tk supaya bisa diuji tanpa membuat
window, dan supaya ``gui.image_view`` fokus pada
interaksi.

Semua fungsi menerima ukuran berupa ``(lebar, tinggi)``
dan bekerja pada koordinat piksel asli.
"""

import math


MIN_SCALE = 0.02

MAX_SCALE = 16.0

EPSILON = 1e-6


def target_size(source_size, scale):
    """
    Ukuran gambar setelah diskalakan.
    """

    width, height = source_size

    return (
        max(int(width * scale), 1),
        max(int(height * scale), 1)
    )


def fit_scale(source_size, area_size, maximum=1.0):
    """
    Skala terbesar (<= ``maximum``) supaya gambar muat
    di dalam area.
    """

    width, height = source_size

    area_width, area_height = area_size

    if width <= 0 or height <= 0:

        return maximum

    if area_width <= 1 or area_height <= 1:

        return maximum

    scale = min(
        area_width / width,
        area_height / height
    )

    return min(max(scale, MIN_SCALE), maximum)


def origin(area_size, image_size, offset):
    """
    Sudut kiri atas gambar dalam koordinat canvas.
    """

    area_width, area_height = area_size

    image_width, image_height = image_size

    return (
        (area_width - image_width) / 2 + offset[0],
        (area_height - image_height) / 2 + offset[1]
    )


def visible_box(
    source_size,
    area_size,
    scale,
    offset
):
    """
    Kotak sumber (piksel asli) yang sedang terlihat.

    Dipakai untuk crop sebelum resize: tanpa ini, zoom
    tinggi akan merender gambar raksasa.
    """

    area_width, area_height = area_size

    source_width, source_height = source_size

    origin_x, origin_y = origin(
        area_size,
        target_size(source_size, scale),
        offset
    )

    safe_scale = max(scale, EPSILON)

    left = int(math.floor(-origin_x / safe_scale))

    top = int(math.floor(-origin_y / safe_scale))

    right = int(math.ceil(
        (area_width - origin_x) / safe_scale
    ))

    bottom = int(math.ceil(
        (area_height - origin_y) / safe_scale
    ))

    return (
        max(left, 0),
        max(top, 0),
        min(max(right, left + 1), source_width),
        min(max(bottom, top + 1), source_height)
    )


def clamp_offset(area_size, image_size, offset):
    """
    Menggeser gambar agar tidak terlalu jauh keluar area.
    """

    area_width, area_height = area_size

    image_width, image_height = image_size

    margin_x = max(
        (image_width - area_width) / 2,
        0
    )

    margin_y = max(
        (image_height - area_height) / 2,
        0
    )

    return [
        max(min(offset[0], margin_x), -margin_x),
        max(min(offset[1], margin_y), -margin_y)
    ]


def clamp_scale(scale, maximum=MAX_SCALE):
    """
    Menahan skala pada batas minimum/maksimum.
    """

    return max(min(scale, maximum), MIN_SCALE)


def zoom_offset(
    offset,
    scale,
    new_scale,
    point,
    area_size
):
    """
    Offset baru supaya titik ``point`` di canvas tetap
    menunjuk piksel yang sama setelah zoom.

    Args:
        offset: offset lama.
        scale: skala lama.
        new_scale: skala baru.
        point: (x, y) dalam koordinat canvas.
        area_size: ukuran area canvas.

    Returns:
        tuple: (offset baru, skala terkoreksi).
    """

    safe_scale = max(scale, EPSILON)

    corrected = max(new_scale, MIN_SCALE)

    applied = corrected / safe_scale

    area_width, area_height = area_size

    anchor_x = point[0] - area_width / 2 - offset[0]

    anchor_y = point[1] - area_height / 2 - offset[1]

    return (
        [
            offset[0] + anchor_x * (1 - applied),
            offset[1] + anchor_y * (1 - applied)
        ],
        corrected
    )
