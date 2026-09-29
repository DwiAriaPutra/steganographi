"""
Panel histogram RGB interaktif.

Layout (judul, legenda, tombol, sumbu bawah, statistik)
menggunakan widget ttk sehingga tidak pernah terpotong;
canvas hanya berisi plot (lihat ``gui.histogram_plot``).

Interaksi:

- klik kiri / ctrl+roda : zoom in di sekitar kursor
- klik kanan            : zoom out
- seret                 : geser sumbu intensitas
- dobel klik            : tampilan penuh

Sumbu X (intensitas) di-zoom; sumbu Y selalu menyesuaikan
puncak data yang terlihat sehingga grafik tidak gepeng.
"""

import tkinter as tk

from tkinter import ttk

from analysis import (
    get_histogram,
    compare_histograms,
    CHANNELS,
)

from .. import histogram_plot as plot

from ..chart import MAX_BIN

from ..histogram_interaction import HistogramInteraction

from ..theme import (
    CANVAS_BG,
    TITLE_FONT,
    AXIS_COLOR,
)

from ..widgets import existing_file


TITLE = "Histogram RGB  -  Cover vs Stego"

CANVAS_HEIGHT = 420

CHANNEL_NAMES = {
    "R": "Red",
    "G": "Green",
    "B": "Blue",
}

SOLID_TEXT = "solid = Cover"

DASHED_TEXT = "dashed = Stego"

AXIS_CAPTION = "Nilai intensitas"

RANGE_CAPTION = "rentang"

HINT = (
    "klik = zoom in   |   klik kanan = zoom out   |   "
    "seret = geser   |   ctrl+roda = zoom"
)

STATS_PREFIX = (
    "Peak cover {}   |   "
    "Peak stego {}   |   "
    "pergeseran histogram: "
    "maks {}   rata-rata {} piksel"
)

MAX_SPAN = float(MAX_BIN)


class HistogramView(ttk.Frame, HistogramInteraction):
    """
    Panel histogram dengan zoom dan pan pada sumbu X.

    Zoom/pan di ``gui.histogram_interaction``.
    """

    def __init__(self, master, session):

        super().__init__(master)

        self.session = session

        self.cover_hist = None

        self.stego_hist = None

        self.x_range = (0.0, MAX_SPAN)

        self.drag_origin = None

        self.drag_range = None

        self.build()

    # ========================================================
    # LAYOUT
    # ========================================================

    def build(self):
        """
        Membangun toolbar, judul, canvas, dan footer.
        """

        self.build_toolbar()

        self.build_title()

        self.canvas = tk.Canvas(
            self,
            background=CANVAS_BG,
            highlightthickness=0,
            width=1,
            height=CANVAS_HEIGHT
        )

        self.canvas.pack(
            fill="both",
            expand=True,
            padx=8,
            pady=(0, 2)
        )

        self.build_footer()

        self.bind_interaction()

    def build_toolbar(self):
        """
        Tombol zoom dan petunjuk.
        """

        bar = ttk.Frame(self)

        bar.pack(
            fill="x",
            padx=8,
            pady=(6, 2)
        )

        for text, command, width in (
            ("+", self.zoom_in, 3),
            ("−", self.zoom_out, 3),
            ("Fit", self.reset, 5),
            ("Zoom LSB", self.zoom_lsb, 9),
        ):

            ttk.Button(
                bar,
                text=text,
                width=width,
                command=command
            ).pack(
                side="left",
                padx=(0, 4)
            )

        ttk.Label(
            bar,
            text=HINT,
            anchor="e",
        ).pack(
            side="right",
            fill="x",
            expand=True
        )

    def build_title(self):
        """
        Judul kiri dan legenda kanan.
        """

        row = ttk.Frame(self)

        row.pack(
            fill="x",
            padx=8,
            pady=(0, 2)
        )

        ttk.Label(
            row,
            text=TITLE,
            font=TITLE_FONT,
        ).pack(side="left")

        legend = ttk.Frame(row)

        legend.pack(side="right")

        for channel in CHANNELS:

            ttk.Label(
                legend,
                text=CHANNEL_NAMES[channel],
                foreground=plot.CHANNEL_COLORS[channel],
            ).pack(
                side="left",
                padx=(10, 0)
            )

        for text in (SOLID_TEXT, DASHED_TEXT):

            ttk.Label(
                legend,
                text=text,
                foreground=AXIS_COLOR,
            ).pack(
                side="left",
                padx=(14, 0)
            )

    def build_footer(self):
        """
        Rentang tampilan, judul sumbu, dan statistik.
        """

        row = ttk.Frame(self)

        row.pack(
            fill="x",
            padx=8
        )

        self.range_label = ttk.Label(
            row,
            text=f"{RANGE_CAPTION}: 0 – 255"
        )

        self.range_label.pack(side="left")

        ttk.Label(
            row,
            text=AXIS_CAPTION,
        ).pack(
            side="left",
            expand=True
        )

        self.status = ttk.Label(
            row,
            text="",
            anchor="e"
        )

        self.status.pack(side="right")

    # ========================================================
    # DATA
    # ========================================================

    def on_resize(self, event=None):
        """
        Redraw saat ukuran canvas berubah.
        """

        self.redraw()

    def redraw(self):
        """
        Memuat ulang histogram dari state sesi.
        """

        cover = self.session.cover_image

        stego = self.session.stego_image

        if not (
            existing_file(cover)
            and existing_file(stego)
        ):

            self.clear()
            return

        try:

            self.cover_hist = get_histogram(cover)

            self.stego_hist = get_histogram(stego)

        except Exception:

            return

        self.draw()

    def clear(self):
        """
        Mengosongkan panel.
        """

        self.cover_hist = None

        self.stego_hist = None

        self.canvas.delete("all")

        self.status.config(text="")

    def draw(self):
        """
        Menggambar plot sesuai rentang tampilan.
        """

        if not (
            self.cover_hist
            and self.stego_hist
        ):

            return

        area = plot.build_area(
            self.canvas,
            (self.cover_hist, self.stego_hist),
            self.x_range
        )

        plot.draw(
            self.canvas,
            area,
            (self.cover_hist, self.stego_hist),
            CHANNELS
        )

        if not area.is_drawable:

            return

        self.update_caption()

        self.update_status()

    def current_area(self):
        """
        PlotArea untuk rentang dan ukuran sekarang.
        """

        return plot.build_area(
            self.canvas,
            (self.cover_hist, self.stego_hist),
            self.x_range
        )

    def update_caption(self):
        """
        Menampilkan rentang intensitas yang terlihat.
        """

        low, high = self.x_range

        self.range_label.config(
            text=f"{RANGE_CAPTION}: {low:.0f} – {high:.0f}"
        )

    def update_status(self):
        """
        Baris statistik pergeseran histogram.
        """

        delta = compare_histograms(
            self.cover_hist,
            self.stego_hist
        )

        self.status.config(
            text=STATS_PREFIX.format(
                f"{delta['peak_cover']:,}",
                f"{delta['peak_stego']:,}",
                f"{delta['max_delta']:,}",
                f"{delta['mean_delta']:.2f}"
            )
        )
