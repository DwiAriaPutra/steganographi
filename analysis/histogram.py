"""
Histogram channel RGB.

Returns:
    dict: {"R": [256 nilai], "G": [256], "B": [256]}
"""

from steg.pixels import open_rgb


CHANNELS = ("R", "G", "B")

BIN_COUNT = 256


def get_histogram(image_path):
    """
    Menghasilkan histogram channel RGB.
    """

    image = open_rgb(image_path)

    flat = image.histogram()

    return {
        channel: flat[
            index * BIN_COUNT:
            (index + 1) * BIN_COUNT
        ]
        for index, channel in enumerate(CHANNELS)
    }


def max_bin(*histograms):
    """
    Nilai bin terbesar dari beberapa histogram.

    Dipakai untuk menentukan skala grafik.
    """

    peak = 1

    for histogram in histograms:

        for channel in CHANNELS:

            peak = max(
                peak,
                max(histogram[channel])
            )

    return peak


def peak_of(histogram):
    """
    Bin tertinggi untuk satu histogram.
    """

    return max(
        max(histogram[channel])
        for channel in CHANNELS
    )


def compare_histograms(
    cover_hist,
    stego_hist
):
    """
    Mengukur seberapa besar histogram bergeser
    setelah pesan disisipkan.

    Returns:
        dict: peak_cover, peak_stego, max_delta, mean_delta.
            Semuanya dalam jumlah piksel.
    """

    deltas = [
        abs(
            cover_hist[channel][index]
            - stego_hist[channel][index]
        )
        for channel in CHANNELS
        for index in range(BIN_COUNT)
    ]

    return {
        "peak_cover": peak_of(cover_hist),
        "peak_stego": peak_of(stego_hist),
        "max_delta": max(deltas),
        "mean_delta": sum(deltas) / len(deltas),
    }
