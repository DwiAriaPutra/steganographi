"""
Penampil gambar untuk GUI.

``ZoomableImage`` adalah frame berisi toolbar zoom dan
viewport gambar. Interaksi zoom/pan ditangani
``gui.image_viewport.ImageViewport``.
"""

from tkinter import ttk

from .image_viewport import ImageViewport


PANEL_HEIGHT = 240

ZOOM_STEP = 1.25


class ZoomableImage(ttk.Frame):
    """
    Frame dengan tombol + / - / Fit / 100% dan viewport.
    """

    def __init__(
        self,
        master,
        text="",
        height=PANEL_HEIGHT
    ):

        super().__init__(master)

        self.placeholder = text

        self.build(height)

    # ========================================================
    # LAYOUT
    # ========================================================

    def build(self, height):
        """
        Membangun toolbar dan viewport.
        """

        self.columnconfigure(0, weight=1)

        self.rowconfigure(1, weight=1)

        bar = ttk.Frame(self)

        bar.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=2,
            pady=(0, 2)
        )

        for label, command, width in (
            ("+", self.zoom_in, 3),
            ("−", self.zoom_out, 3),
            ("Fit", self.fit, 4),
            ("100%", self.actual, 5),
        ):

            ttk.Button(
                bar,
                text=label,
                width=width,
                command=command
            ).pack(
                side="left",
                padx=(0, 3)
            )

        self.zoom_label = ttk.Label(
            bar,
            text="",
            anchor="e"
        )

        self.zoom_label.pack(
            side="right",
            fill="x",
            expand=True
        )

        self.viewport = ImageViewport(
            self,
            height=height,
            placeholder=self.placeholder
        )

        self.viewport.on_zoom = self.show_scale

        self.viewport.canvas.grid(
            row=1,
            column=0,
            sticky="nsew"
        )

    def show_scale(self, scale):
        """
        Menampilkan persentase zoom.
        """

        self.zoom_label.config(
            text=f"{scale * 100:.0f}%"
        )

    # ========================================================
    # DELEGASI KE VIEWPORT
    # ========================================================

    @property
    def canvas(self):
        return self.viewport.canvas

    @property
    def source(self):
        return self.viewport.source

    @property
    def photo(self):
        return self.viewport.photo

    @property
    def scale(self):
        return self.viewport.scale

    @property
    def offset(self):
        return self.viewport.offset

    def set_image(self, image):
        return self.viewport.set_image(image)

    def clear(self, text=""):
        self.viewport.clear(text)

        self.zoom_label.config(text="")

    def fit(self, event=None):
        return self.viewport.fit()

    def actual(self):
        return self.viewport.actual()

    def zoom_in(self):
        return self.viewport.zoom_in()

    def zoom_out(self):
        return self.viewport.zoom_out()

    def zoom_at(self, x=None, y=None, factor=ZOOM_STEP):
        return self.viewport.zoom_at(x, y, factor)

    def on_press(self, event):
        return self.viewport.on_press(event)

    def on_release(self, event=None):
        return self.viewport.on_release()

    def on_drag(self, event):
        return self.viewport.on_drag(event)
