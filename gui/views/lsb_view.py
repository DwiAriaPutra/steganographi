"""
Panel analisis LSB.

Tiga penampil: LSB plane cover, LSB plane stego, dan
peta piksel yang LSB-nya berubah.

Ukuran thumbnail dibatasi satu kotak yang sama supaya
tiga gambar sejajar dan tidak gepeng.
"""

from tkinter import ttk

from analysis import (
    get_lsb_plane,
    get_lsb_difference,
)

from ..theme import EMPTY_TEXT

from ..image_view import ZoomableImage

from ..widgets import (
    label_frame,
    existing_file,
)


PANEL_HEIGHT = 340

SUMMARY = (
    "Pixel putih = ada channel yang LSB-nya berubah "
    "karena pesan disisipkan."
)


class LsbView(ttk.Frame):
    """
    Panel LSB analysis.
    """

    def __init__(
        self,
        master,
        session
    ):

        super().__init__(master)

        self.session = session

        self.cover_label = None

        self.stego_label = None

        self.difference_label = None

        self.build()

    def build(self):
        """
        Membangun layout tiga penampil.
        """

        container = ttk.Frame(
            self,
            padding=8
        )

        container.pack(
            fill="both",
            expand=True
        )

        top = ttk.Frame(container)

        top.pack(
            fill="both",
            expand=True
        )

        cover_frame = label_frame(
            top,
            "Cover LSB Plane",
            height=PANEL_HEIGHT
        )

        cover_frame.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 5)
        )

        self.cover_label = ZoomableImage(
            cover_frame,
            EMPTY_TEXT
        )

        self.cover_label.pack(
            fill="both",
            expand=True
        )

        stego_frame = label_frame(
            top,
            "Stego LSB Plane",
            height=PANEL_HEIGHT
        )

        stego_frame.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(5, 0)
        )

        self.stego_label = ZoomableImage(
            stego_frame,
            EMPTY_TEXT
        )

        self.stego_label.pack(
            fill="both",
            expand=True
        )

        difference_frame = label_frame(
            container,
            "LSB Difference",
            height=PANEL_HEIGHT
        )

        difference_frame.pack(
            fill="both",
            expand=True,
            pady=(10, 0)
        )

        self.difference_label = ZoomableImage(
            difference_frame,
            EMPTY_TEXT
        )

        self.difference_label.pack(
            fill="both",
            expand=True
        )

        ttk.Label(
            container,
            text=SUMMARY
        ).pack(anchor="w", pady=(6, 0))

    def redraw(self, on_error=None):
        """
        Menghitung ulang LSB plane dari state sesi.
        """

        cover = self.session.cover_image

        stego = self.session.stego_image

        if not (
            existing_file(cover)
            and existing_file(stego)
        ):

            return

        try:

            cover_lsb = get_lsb_plane(cover)

            stego_lsb = get_lsb_plane(stego)

            difference = get_lsb_difference(
                cover,
                stego
            )

        except Exception as error:

            if on_error:

                on_error(error)

            return

        self.display(
            cover_lsb,
            stego_lsb,
            difference
        )

    def display(
        self,
        cover_lsb,
        stego_lsb,
        difference
    ):
        """
        Menyerahkan hasil LSB analysis ke penampil.

        Ukuran menyesuaikan label, aspectratio dijaga.
        """

        self.cover_label.set_image(cover_lsb)

        self.stego_label.set_image(stego_lsb)

        self.difference_label.set_image(difference)
