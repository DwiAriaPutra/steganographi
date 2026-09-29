"""
Viewport gambar: canvas tempat gambar digambar.

Menyimpan gambar sumber, skala, dan posisi, lalu merender
**hanya bagian yang terlihat** sehingga zoom tinggi tetap
ringan.

Zoom dan pan ditangani mixin
``gui.image_interaction.ImageInteraction``.
Tidak bergantung pada chrome: ``gui.image_view``
membungkus viewport ini dengan toolbar.
"""

import tkinter as tk

from PIL import Image, ImageTk

from . import image_math as geometry

from .image_interaction import ImageInteraction

from .theme import (
    IMAGE_BG,
    IMAGE_PLACEHOLDER_COLOR,
)


MIN_SCALE = geometry.MIN_SCALE

MAX_SCALE = geometry.MAX_SCALE


class ImageViewport(ImageInteraction):
    """
    Canvas penampil gambar.
    """

    def __init__(
        self,
        master,
        height=240,
        placeholder=""
    ):

        self.source = None

        self.scale = 1.0

        self.offset = [0.0, 0.0]

        self.photo = None

        self.built = False

        self.drag_origin = None

        self.drag_offset = None

        self.on_zoom = None

        self.canvas = tk.Canvas(
            master,
            background=IMAGE_BG,
            highlightthickness=0,
            width=1,
            height=height
        )

        self.show_placeholder(placeholder)

        self.bind_events()

    # ========================================================
    # PLACEHOLDER
    # ========================================================

    def show_placeholder(self, text):
        """
        Menampilkan teks saat belum ada gambar.
        """

        self.canvas.delete("all")

        if not text:

            return

        self.canvas.create_text(
            10,
            10,
            text=text,
            anchor="nw",
            fill=IMAGE_PLACEHOLDER_COLOR
        )

    # ========================================================
    # DATA
    # ========================================================

    def set_image(self, image):
        """
        Mengganti gambar dan memuatnya penuh.
        """

        self.source = image

        self.built = False

        self.drag_origin = None

        self.canvas.delete("all")

        self.on_resize()

    def clear(self, text=""):
        """
        Mengosongkan viewport.
        """

        self.source = None

        self.photo = None

        self.built = False

        self.show_placeholder(text)

    def on_resize(self, event=None):
        """
        Menyesuaikan gambar dengan area terbaru.

        Saat pertama kali dibangun gambar otomatis "fit";
        sesudahnya posisi zoom pengguna dipertahankan.
        """

        if self.source is None:

            return

        if not self.built:

            self.fit()
            return

        self.offset = geometry.clamp_offset(
            self.area_size(),
            self.target_size(),
            self.offset
        )

        self.render()

    # ========================================================
    # GEOMETRI
    # ========================================================

    def area_size(self):
        """
        Ukuran area canvas yang terpakai.
        """

        return (
            self.canvas.winfo_width(),
            self.canvas.winfo_height()
        )

    def target_size(self):
        """
        Ukuran gambar pada skala sekarang.
        """

        return geometry.target_size(
            self.source.size,
            self.scale
        )

    # ========================================================
    # RENDER
    # ========================================================

    def render(self):
        """
        Menggambar bagian gambar yang terlihat saja.

        Crop pada resolusi penuh lalu resize, sehingga biaya
        render tetap kecil pada zoom setinggi apa pun.
        """

        if self.source is None:

            return

        self.canvas.delete("all")

        area = self.area_size()

        if area[0] <= 1 or area[1] <= 1:

            return

        box = geometry.visible_box(
            self.source.size,
            area,
            self.scale,
            self.offset
        )

        if box[2] <= box[0] or box[3] <= box[1]:

            self.photo = None
            return

        crop = self.source.crop(box)

        size = (
            max(int(round(
                (box[2] - box[0]) * self.scale
            )), 1),
            max(int(round(
                (box[3] - box[1]) * self.scale
            )), 1)
        )

        self.photo = ImageTk.PhotoImage(
            crop.resize(size, Image.LANCZOS)
        )

        origin_x, origin_y = geometry.origin(
            area,
            self.target_size(),
            self.offset
        )

        self.canvas.create_image(
            origin_x + box[0] * self.scale,
            origin_y + box[1] * self.scale,
            image=self.photo,
            anchor="nw"
        )

        if self.on_zoom:

            self.on_zoom(self.scale)

    # ========================================================
    # TAMPILAN
    # ========================================================

    def fit(self, event=None):
        """
        Menyesuaikan gambar agar muat seluruh area.
        """

        if self.source is None:

            return

        self.scale = geometry.fit_scale(
            self.source.size,
            self.area_size(),
            MAX_SCALE
        )

        self.offset = [0.0, 0.0]

        self.built = True

        self.render()
