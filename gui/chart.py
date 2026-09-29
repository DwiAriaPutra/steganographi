"""
Geometri area plot histogram.

Pisahkan logika numerik dari perintah canvas supaya
``gui.views.histogram_view`` hanya dealing dengan
koordinat dan label.

Plot mendukung rentang tampilan (zoom) pada sumbu X
(intensitas); sumbu Y selalu dihitung dari puncak data
yang terlihat sehingga grafik tidak pernah gepeng.
"""

import math

from .ticks import (
    nice_ceiling,
    nice_step,
    format_tick,
    TARGET_Y_TICKS,
)


MARGIN_LEFT = 62

MARGIN_RIGHT = 24

MARGIN_TOP = 18

MARGIN_BOTTOM = 34

BIN_COUNT = 256

MAX_BIN = BIN_COUNT - 1

MIN_SIZE = 160

TARGET_X_TICKS = 8

EPSILON = 1e-9


class PlotArea:
    """
    Area gambar beserta pemetaan nilai -> koordinat.

    ``x_range`` dan ``y_range`` menentukan bagian data
    yang terlihat; nilai di luar rentang tidak digambar.
    """

    def __init__(
        self,
        width,
        height,
        peak,
        x_range=None,
        y_range=None
    ):

        self.width = width

        self.height = height

        self.x_low, self.x_high = x_range or (0.0, float(MAX_BIN))

        if y_range:

            self.y_low, self.y_high = y_range

        else:

            self.y_low, self.y_high = 0.0, float(
                nice_ceiling(peak)
            )

        self.graph_width = (
            width
            - MARGIN_LEFT
            - MARGIN_RIGHT
        )

        self.graph_height = (
            height
            - MARGIN_TOP
            - MARGIN_BOTTOM
        )

    @property
    def is_drawable(self):
        """
        True bila canvas cukup besar untuk digambar.
        """

        return (
            self.width >= MIN_SIZE
            and self.height >= MIN_SIZE
        )

    # ========================================================
    # TITIK DI CANVAS
    # ========================================================

    @property
    def x0(self):
        return MARGIN_LEFT

    @property
    def y0(self):
        """
        Garis dasar grafik.
        """

        return self.height - MARGIN_BOTTOM

    @property
    def x1(self):
        return self.width - MARGIN_RIGHT

    @property
    def y1(self):
        return MARGIN_TOP

    def x_at(self, value):
        """
        Koordinat x untuk nilai intensitas.
        """

        span = max(
            self.x_high - self.x_low,
            EPSILON
        )

        return self.x0 + (
            (value - self.x_low) / span
        ) * self.graph_width

    def y_at(self, value):
        """
        Koordinat y untuk jumlah piksel.
        """

        span = max(
            self.y_high - self.y_low,
            EPSILON
        )

        return self.y0 - (
            (value - self.y_low) / span
        ) * self.graph_height

    def value_at_x(self, x):
        """
        Kebalikan dari ``x_at``: koordinat -> intensitas.
        """

        span = max(
            self.x_high - self.x_low,
            EPSILON
        )

        ratio = (
            (x - self.x0) / max(
                self.graph_width,
                EPSILON
            )
        )

        return (
            self.x_low
            + ratio * span
        )

    def value_at_y(self, y):
        """
        Kebalikan dari ``y_at``: koordinat -> jumlah piksel.
        """

        span = max(
            self.y_high - self.y_low,
            EPSILON
        )

        ratio = (
            (self.y0 - y) / max(
                self.graph_height,
                EPSILON
            )
        )

        return (
            self.y_low
            + ratio * span
        )

    # ========================================================
    # DATA
    # ========================================================

    def visible_slice(self, values):
        """
        Memotong channel histogram ke rentang X terlihat.

        Returns:
            list[int]: nilai pada bin yang terlihat.
    """

        low = max(
            int(math.floor(self.x_low)),
            0
        )

        high = min(
            int(math.ceil(self.x_high)),
            MAX_BIN
        )

        if high < low:

            return []

        return values[low:high + 1]

    def channel_points(self, values):
        """
        Mengubah channel histogram menjadi list koordinat
        [x0, y0, x1, y1, ...] untuk rentang yang terlihat.
        """

        low = max(
            int(math.floor(self.x_low)),
            0
        )

        points = []

        for index, value in enumerate(
            self.visible_slice(values),
            start=low
        ):

            points.extend((
                self.x_at(index),
                self.y_at(value)
            ))

        return points

    def peak_in_range(self, *histograms):
        """
        Bin tertinggi pada rentang X yang terlihat.
        """

        peak = 0.0

        for histogram in histograms:

            for channel in histogram:

                values = self.visible_slice(
                    histogram[channel]
                )

                if values:

                    peak = max(
                        peak,
                        max(values)
                    )

        return peak

    # ========================================================
    # TICK
    # ========================================================

    def x_ticks(self):
        """
        Tick sumbu X sesuai rentang terlihat.
        """

        span = self.x_high - self.x_low

        step = max(
            nice_step(span, TARGET_X_TICKS),
            1
        )

        ticks = []

        value = self.x_low

        while value <= self.x_high + EPSILON:

            ticks.append((
                self.x_at(value),
                format_tick(value)
            ))

            value += step

        if not ticks:

            ticks.append((
                self.x_at(self.x_low),
                format_tick(self.x_low)
            ))

        return ticks

    def y_ticks(self):
        """
        Tick sumbu Y sesuai rentang terlihat.
        """

        step = nice_step(
            self.y_high - self.y_low,
            TARGET_Y_TICKS
        )

        ticks = []

        value = self.y_low

        while value <= self.y_high + EPSILON:

            ticks.append((
                self.y_at(value),
                format_tick(value)
            ))

            value += step

        if not ticks:

            ticks.append((
                self.y_at(self.y_low),
                format_tick(self.y_low)
            ))

        return ticks

    def to_view(self, x_range, y_range):
        """
        Membuat PlotArea baru dengan rentang baru.
        """

        return PlotArea(
            self.width,
            self.height,
            0,
            x_range,
            y_range
        )
