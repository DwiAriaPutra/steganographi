"""
Tab Analysis.

Berisi pratinjau cover/stego, metrik MSE + PSNR, dan
sub-notebook berisi histogram serta LSB analysis.

Seluruh isi dibungkus ``ScrollableFrame`` supaya tetap
utuh pada jendela kecil.
"""

from PIL import Image

from tkinter import ttk

from analysis import calculate_metrics

from ..scroll import ScrollableFrame

from ..theme import PLACEHOLDER_TEXT

from ..image_view import ZoomableImage

from ..widgets import (
    label_frame,
    existing_file,
)

from .histogram_view import HistogramView

from .lsb_view import LsbView


PREVIEW_HEIGHT = 300

NOTEBOOK_HEIGHT = 720

PSNR_INFINITY = "∞ dB"

METRIC_CAPTION = "Selisih nilai channel antara cover dan stego image"


class AnalysisTab(ttk.Frame):
    """
    Tab analisis kualitas steganografi.
    """

    def __init__(
        self,
        master,
        session,
        on_error=None,
        on_lsb_error=None
    ):

        super().__init__(master)

        self.session = session

        self.on_error = on_error

        self.on_lsb_error = on_lsb_error

        self.histogram_view = None

        self.lsb_view = None

        self.build()

    def build(self):
        """
        Membangun layout tab analysis.
        """

        self.scroller = ScrollableFrame(
            self,
            padding=15
        )

        self.scroller.pack(
            fill="both",
            expand=True
        )

        container = self.scroller.body

        self.build_previews(container)

        self.build_metrics(container)

        self.build_sub_notebook(container)

    def build_previews(self, container):
        """
        Dua penampil gambar cover dan stego.
        """

        section = ttk.Frame(container)

        section.pack(fill="x")

        cover_frame = label_frame(
            section,
            "Cover Image",
            height=PREVIEW_HEIGHT
        )

        cover_frame.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 5)
        )

        self.cover_preview = ZoomableImage(
            cover_frame,
            PLACEHOLDER_TEXT
        )

        self.cover_preview.pack(
            fill="both",
            expand=True
        )

        stego_frame = label_frame(
            section,
            "Stego Image",
            height=PREVIEW_HEIGHT
        )

        stego_frame.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(5, 0)
        )

        self.stego_preview = ZoomableImage(
            stego_frame,
            PLACEHOLDER_TEXT
        )

        self.stego_preview.pack(
            fill="both",
            expand=True
        )

    def build_metrics(self, container):
        """
        Baris metrik MSE dan PSNR.
        """

        frame = label_frame(
            container,
            "Image Quality"
        )

        frame.pack(
            fill="x",
            pady=(10, 10)
        )

        ttk.Label(
            frame,
            text=METRIC_CAPTION
        ).pack(anchor="w")

        row = ttk.Frame(frame)

        row.pack(
            fill="x",
            pady=(6, 0)
        )

        self.mse_value = build_metric(
            row,
            "MSE"
        )

        self.psnr_value = build_metric(
            row,
            "PSNR"
        )

    def build_sub_notebook(self, container):
        """
        Notebook histogram dan LSB analysis.
        """

        holder = ttk.Frame(
            container,
            width=1,
            height=NOTEBOOK_HEIGHT
        )

        # propagasi dimatikan agar tinggi notebook tidak
        # ikut menyusut mengikuti isi tab
        holder.pack_propagate(False)

        holder.pack(fill="x")

        # width=1 supaya notebook tidak memaksa tab melebihi
        # lebar area scroll
        notebook = ttk.Notebook(
            holder,
            width=1,
            height=1
        )

        notebook.pack(
            fill="both",
            expand=True
        )

        histogram_tab = ttk.Frame(notebook)

        lsb_tab = ttk.Frame(notebook)

        notebook.add(
            histogram_tab,
            text="Histogram"
        )

        notebook.add(
            lsb_tab,
            text="LSB Analysis"
        )

        self.histogram_view = HistogramView(
            histogram_tab,
            self.session
        )

        self.histogram_view.pack(
            fill="both",
            expand=True
        )

        self.lsb_view = LsbView(
            lsb_tab,
            self.session
        )

        self.lsb_view.pack(
            fill="both",
            expand=True
        )

    def refresh(self):
        """
        Memuat ulang seluruh isi tab dari state sesi.
        """

        if not self.session.is_ready:

            return

        if not (
            existing_file(
                self.session.cover_image
            )
            and existing_file(
                self.session.stego_image
            )
        ):

            return

        try:

            self.refresh_previews()

            self.refresh_metrics()

        except Exception as error:

            if self.on_error:

                self.on_error(error)

            return

        self.histogram_view.redraw()

        self.lsb_view.redraw(self.on_lsb_error)

    def refresh_previews(self):
        """
        Menyerahkan gambar cover dan stego ke penampil.

        Penampil yang menyesuaikan ukurannya sendiri,
        jadi gambar tidak pernah terpotong.
        """

        self.cover_preview.set_image(
            open_image(
                self.session.cover_image
            )
        )

        self.stego_preview.set_image(
            open_image(
                self.session.stego_image
            )
        )

    def refresh_metrics(self):
        """
        Menghitung dan menampilkan MSE + PSNR.
        """

        mse, psnr = calculate_metrics(
            self.session.cover_image,
            self.session.stego_image
        )

        self.mse_value.config(
            text=f"{mse:.6f}"
        )

        if psnr == float("inf"):

            self.psnr_value.config(
                text=PSNR_INFINITY
            )

        else:

            self.psnr_value.config(
                text=f"{psnr:.2f} dB"
            )


def build_metric(parent, title):
    """
    Membuat satu blok metrik (judul + nilai besar).
    """

    frame = ttk.Frame(parent)

    frame.pack(
        side="left",
        expand=True
    )

    ttk.Label(
        frame,
        text=title
    ).pack()

    value = ttk.Label(
        frame,
        text="-",
        style="Metric.TLabel"
    )

    value.pack()

    return value


def open_image(image_path):
    """
    Membuka gambar sebagai RGB untuk ditampilkan.
    """

    return Image.open(image_path).convert("RGB")
