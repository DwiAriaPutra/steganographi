"""
Interaksi zoom & pan untuk histogram.

Mixin ini (``HistogramInteraction``) dipakai
``gui.views.histogram_view.HistogramView`` dan
memerlukan dari kelas induk:

- ``canvas``
- ``x_range`` (rentang intensitas yang terlihat)
- ``draw()``, ``current_area()``
- ``cover_hist``, ``stego_hist``
"""

from .chart import MAX_BIN


ZOOM_FACTOR = 2.0

MIN_SPAN = 4.0

MAX_SPAN = float(MAX_BIN)

LSB_HIGH = 32.0


class HistogramInteraction:
    """
    Zoom pada sumbu intensitas dan pan dengan menyeret.
    """

    def bind_interaction(self):
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
            self.reset
        )

        self.canvas.bind(
            "<Control-MouseWheel>",
            self.on_ctrl_wheel
        )

        self.canvas.bind(
            "<Button-4>",
            self.on_wheel_linux
        )

        self.canvas.bind(
            "<Button-5>",
            self.on_wheel_linux
        )

    # ========================================================
    # TAMPILAN
    # ========================================================

    def reset(self, event=None):
        """
        Kembali ke tampilan penuh.
        """

        self.x_range = (0.0, MAX_SPAN)

        self.draw()

    def zoom_lsb(self):
        """
        Zoom ke rentang LSB (0 - 31).
        """

        self.x_range = (0.0, LSB_HIGH)

        self.draw()

    def zoom_in(self):
        """
        Zoom in di tengah area.
        """

        self.zoom_at(None, ZOOM_FACTOR)

    def zoom_out(self):
        """
        Zoom out di tengah area.
        """

        self.zoom_at(None, 1 / ZOOM_FACTOR)

    # ========================================================
    # PAN
    # ========================================================

    def on_press(self, event):
        """
        Klik kiri: tandai titik pan dan zoom.
        """

        self.drag_origin = (event.x, event.y)

        self.drag_range = self.x_range

    def on_release(self, event=None):
        """
        Selesai pan.
        """

        self.drag_origin = None

        self.drag_range = None

    def on_drag(self, event):
        """
        Seret mouse: menggeser rentang tampilan.
        """

        if self.drag_origin is None:

            return

        area = self.current_area()

        span = self.drag_range[1] - self.drag_range[0]

        shift = -(event.x - self.drag_origin[0]) / max(
            area.graph_width, 1
        ) * span

        self.x_range = self._clamp((
            self.drag_range[0] + shift,
            self.drag_range[1] + shift
        ))

        self.draw()

    # ========================================================
    # ZOOM
    # ========================================================

    def on_zoom_out(self, event=None):
        """
        Klik kanan: zoom out di posisi kursor.
        """

        self.zoom_at(
            event.x if event else None,
            1 / ZOOM_FACTOR
        )

    def on_ctrl_wheel(self, event):
        """
        Ctrl + roda: zoom di posisi kursor.
        """

        self.zoom_at(
            event.x,
            ZOOM_FACTOR
            if event.delta < 0
            else 1 / ZOOM_FACTOR
        )

        return "break"

    def on_wheel_linux(self, event):
        """
        Roda Linux (tombol 4/5): zoom di posisi kursor.
        """

        self.zoom_at(
            event.x,
            ZOOM_FACTOR
            if event.num == 4
            else 1 / ZOOM_FACTOR
        )

        return "break"

    def zoom_at(self, x=None, factor=ZOOM_FACTOR):
        """
        Memperbesar atau memperkecil di sekitar sumbu x kursor.
        """

        if not (
            self.cover_hist
            and self.stego_hist
        ):

            return

        area = self.current_area()

        if not area.is_drawable:

            return

        anchor = area.value_at_x(
            area.width / 2 if x is None else x
        )

        self.x_range = self._clamp(
            self._scale(self.x_range, anchor, factor)
        )

        self.draw()

    # ========================================================
    # RENTANG
    # ========================================================

    def _scale(self, span, anchor, factor):
        """
        Mengubah lebar rentang di sekitar ``anchor``.
        """

        low, high = span

        new_low = anchor - (anchor - low) / factor

        new_high = anchor + (high - anchor) / factor

        if new_high - new_low < MIN_SPAN:

            center = (new_low + new_high) / 2

            new_low = center - MIN_SPAN / 2

            new_high = center + MIN_SPAN / 2

        return (new_low, new_high)

    def _clamp(self, span):
        """
        Menahan rentang agar tidak keluar dari 0 - 255
        dan tidak terbalik.
        """

        low, high = span

        width = high - low

        if width <= 0:

            return (0.0, MAX_SPAN)

        if low < 0:

            low = 0.0
            high = width

        if high > MAX_SPAN:

            high = MAX_SPAN
            low = max(high - width, 0.0)

        return (low, high)
