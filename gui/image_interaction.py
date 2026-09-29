"""
Interaksi zoom & pan untuk viewport gambar.

Dipisah dari ``gui.image_viewport`` supaya kelas
viewport tetap fokus pada render.

Mixin ini (``ImageInteraction``) memakai atribut dan
metode berikut dari kelas induk:

- ``source``, ``scale``, ``offset``, ``built``
- ``drag_origin``, ``drag_offset``
- ``area_size()``, ``target_size()``, ``render()``
"""

from . import image_math as geometry


ZOOM_FACTOR = 1.25

MAX_SCALE = geometry.MAX_SCALE


class ImageInteraction:
    """
    Semua penanganan mouse untuk zoom dan pan.
    """

    # ========================================================
    # EVENTS
    # ========================================================

    def bind_events(self):
        """
        Menghubungkan event mouse ke zoom dan pan.
        """

        self.canvas.bind(
            "<Configure>",
            self.on_resize
        )

        self.canvas.bind(
            "<Button-1>",
            self.on_press
        )

        self.canvas.bind(
            "<ButtonRelease-1>",
            self.on_release
        )

        self.canvas.bind(
            "<B1-Motion>",
            self.on_drag
        )

        self.canvas.bind(
            "<Button-3>",
            self.on_zoom_out
        )

        self.canvas.bind(
            "<Double-Button-1>",
            self.fit
        )

        self.canvas.bind(
            "<Control-MouseWheel>",
            self.on_ctrl_wheel
        )

    def on_press(self, event):
        """
        Klik kiri: mulai pan.
        """

        self.drag_origin = (event.x, event.y)

        self.drag_offset = list(self.offset)

    def on_release(self, event=None):
        """
        Selesai pan.
        """

        self.drag_origin = None

        self.drag_offset = None

    def on_drag(self, event):
        """
        Seret mouse: menggeser gambar.
        """

        if self.drag_origin is None:

            return

        self.offset = geometry.clamp_offset(
            self.area_size(),
            self.target_size(),
            [
                self.drag_offset[0] + event.x - self.drag_origin[0],
                self.drag_offset[1] + event.y - self.drag_origin[1],
            ]
        )

        self.render()

    def on_zoom_out(self, event=None):
        """
        Klik kanan: zoom out di posisi kursor.
        """

        self.zoom_at(
            event.x if event else None,
            event.y if event else None,
            1 / ZOOM_FACTOR
        )

    def on_ctrl_wheel(self, event):
        """
        Ctrl + roda: zoom di posisi kursor.
        """

        self.zoom_at(
            event.x,
            event.y,
            ZOOM_FACTOR
            if event.delta < 0
            else 1 / ZOOM_FACTOR
        )

        return "break"

    # ========================================================
    # ZOOM
    # ========================================================

    def zoom_in(self):
        """
        Zoom in di tengah area.
        """

        self.zoom_at(None, None, ZOOM_FACTOR)

    def zoom_out(self):
        """
        Zoom out di tengah area.
        """

        self.zoom_at(None, None, 1 / ZOOM_FACTOR)

    def actual(self):
        """
        Menampilkan gambar pada ukuran aslinya (100%).
        """

        if self.source is None:

            return

        self.scale = 1.0

        self.built = True

        self.on_resize()

    def zoom_at(
        self,
        x=None,
        y=None,
        factor=ZOOM_FACTOR
    ):
        """
        Zoom di sekitar titik kursor (titik itu diam).
        """

        if self.source is None or factor is None:

            return

        area = self.area_size()

        if area[0] <= 1 or area[1] <= 1:

            return

        point = (
            area[0] / 2 if x is None else x,
            area[1] / 2 if y is None else y
        )

        offset, scale = geometry.zoom_offset(
            self.offset,
            self.scale,
            self.scale * factor,
            point,
            area
        )

        self.scale = geometry.clamp_scale(
            scale,
            MAX_SCALE
        )

        self.offset = geometry.clamp_offset(
            area,
            geometry.target_size(
                self.source.size,
                self.scale
            ),
            offset
        )

        self.built = True

        self.render()
