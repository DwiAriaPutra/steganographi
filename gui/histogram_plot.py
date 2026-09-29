"""
Penggambar plot histogram ke canvas.

Pisahkan perintah canvas dari layout dan interaksi
(``gui.views.histogram_view``) supaya file ini hanya
berisi penggambaran, dan tick/kurva bisa diuji tanpa
membuat window.
"""

from .chart import PlotArea

from .theme import (
    GRID_COLOR,
    AXIS_COLOR,
)


CHANNEL_COLORS = {
    "R": "#e03131",
    "G": "#2f9e44",
    "B": "#1971c2",
}

SOLID_DASH = None

DASHED_DASH = (4, 3)

LINE_WIDTH = 2

X_TICK_GAP = 8

Y_TICK_GAP = 8


def build_area(canvas, histograms, x_range):
    """
    Membuat PlotArea dengan sumbu Y mengikuti puncak data
    yang sedang terlihat.
    """

    width = canvas.winfo_width()

    height = canvas.winfo_height()

    area = PlotArea(
        width,
        height,
        0,
        x_range
    )

    peak = area.peak_in_range(*histograms)

    return PlotArea(
        width,
        height,
        peak,
        x_range
    )


def draw(canvas, area, histograms, channels):
    """
    Menggambar grid, sumbu, dan seluruh channel.
    """

    canvas.delete("all")

    if not area.is_drawable:

        return

    _draw_grid(canvas, area)

    _draw_axes(canvas, area)

    for dashed in (False, True):

        for channel in channels:

            histogram = (
                histograms[1] if dashed
                else histograms[0]
            )

            _draw_channel(
                canvas,
                area,
                histogram[channel],
                channel,
                dashed
            )


def _draw_grid(canvas, area):
    """
    Garis bantu horizontal.
    """

    for y, _ in area.y_ticks():

        canvas.create_line(
            area.x0,
            y,
            area.x1,
            y,
            fill=GRID_COLOR
        )


def _draw_axes(canvas, area):
    """
    Sumbu X dan Y beserta label tick.
    """

    canvas.create_line(
        area.x0,
        area.y0,
        area.x1,
        area.y0,
        fill=AXIS_COLOR
    )

    canvas.create_line(
        area.x0,
        area.y0,
        area.x0,
        area.y1,
        fill=AXIS_COLOR
    )

    for y, label in area.y_ticks():

        canvas.create_text(
            area.x0 - Y_TICK_GAP,
            y,
            text=label,
            anchor="e",
            fill=AXIS_COLOR
        )

    for x, label in area.x_ticks():

        canvas.create_text(
            x,
            area.y0 + X_TICK_GAP,
            text=label,
            fill=AXIS_COLOR
        )


def _draw_channel(
    canvas,
    area,
    values,
    channel,
    dashed=False
):
    """
    Satu garis channel histogram.

    Garis solid = cover, garis putus-putus = stego.
    """

    points = area.channel_points(values)

    if len(points) < 4:

        return

    canvas.create_line(
        points,
        fill=CHANNEL_COLORS[channel],
        width=LINE_WIDTH,
        smooth=True,
        dash=(
            DASHED_DASH if dashed
            else SOLID_DASH
        )
    )
