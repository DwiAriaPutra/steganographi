"""
Kontainer yang bisa di-scroll.

Isi tab diletakkan di dalam ``body`` lalu digeser dengan
``place`` (bukan canvas window-item), sehingga isi tetap
tergambar utuh di semua backend X/Wayland.

Lebar body mengikuti area tampilan lewat ``relwidth=1.0``,
bukan pixel eksplisit, supaya tidak ada umpan balik antara
lebar body dan lebar container.

Scrollbar hanya muncul bila ada yang terpotong.
"""

from tkinter import ttk


WHEEL_STEP = 48

BAR_STEP = 48

LINE_STEP = 16

EPSILON = 0.5


def _step_for(units, viewport):
    """
    Mengubah satuan scrollbar menjadi piksel.
    """

    if units == "pages":

        return viewport

    if units == "lines":

        return LINE_STEP

    return BAR_STEP


class ScrollableFrame(ttk.Frame):
    """
    Frame dengan area scroll vertikal.

    Pemakaian::

        scroller = ScrollableFrame(parent, padding=15)
        scroller.pack(fill="both", expand=True)
        scroller.body  <- taruh widget di sini
    """

    def __init__(
        self,
        master,
        padding=0
    ):

        super().__init__(master)

        self.columnconfigure(0, weight=1)

        self.rowconfigure(0, weight=1)

        self.viewport = ttk.Frame(self)

        self.viewport.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        self.scrollbar = ttk.Scrollbar(
            self,
            orient="vertical",
            command=self.scroll
        )

        self.body = ttk.Frame(
            self.viewport,
            padding=padding
        )

        self.offset = 0.0

        self.viewport_height = 1

        self.content = 1

        self._wheel_depth = 0

        self._updating = False

        self.body.bind(
            "<Configure>",
            self.sync
        )

        self.bind("<Configure>", self.sync)

        self.bind("<Enter>", self._enter)
        self.bind("<Leave>", self._leave)

        self.sync()

    def pack_body(self, **options):
        """
        Memasang body dengan opsi standar.
        """

        self.body.pack(
            fill="both",
            expand=True,
            **options
        )

    # ========================================================
    # LAYOUT
    # ========================================================

    def place_body(self):
        """
        Menempatkan body selebar viewport, digeser
        sebesar offset scroll saat ini.
        """

        self.body.place(
            x=0,
            y=-int(self.offset),
            relwidth=1.0
        )

    def sync(self, event=None):
        """
        Menyamakan ukuran isi, viewport, dan scrollbar.
        """

        if self._updating:

            return

        self._updating = True

        try:

            self.update_idletasks()

            self.viewport_height = max(
                self.viewport.winfo_height(),
                1
            )

            self.content = max(
                self.body.winfo_reqheight(),
                self.body.winfo_height(),
                1
            )

            self.offset = max(
                min(self.offset, self.max_offset()),
                0
            )

            self.place_body()

            self.refresh_scrollbar()

        finally:

            self._updating = False

    def refresh_scrollbar(self):
        """
        Menampilkan atau menyembunyikan scrollbar sesuai
        kebutuhan, lalu menyetel posisi thumb.
        """

        needed = self.max_offset() > EPSILON

        mapped = bool(
            self.scrollbar.winfo_ismapped()
        )

        if needed and not mapped:

            self.scrollbar.grid(
                row=0,
                column=1,
                sticky="ns"
            )

        elif not needed and mapped:

            self.scrollbar.grid_remove()

        if self.scrollbar.winfo_ismapped():

            self.scrollbar.set(
                self.first(),
                self.last()
            )

    def max_offset(self):
        """
        Batas scroll paling bawah.
        """

        return max(
            self.content - self.viewport_height,
            0
        )

    def span(self):
        """
        Panjang thumb scrollbar (0..1).
        """

        if self.content <= 0:

            return 1.0

        return min(
            self.viewport_height / self.content,
            1.0
        )

    def first(self):
        """
        Posisi thumb atas (0..1).
        """

        if self.content <= 0:

            return 0.0

        return max(
            min(self.offset / self.content, 1.0),
            0.0
        )

    def last(self):
        """
        Posisi thumb bawah (0..1).
        """

        if self.content <= 0:

            return 1.0

        return max(
            min(
                (self.offset + self.viewport_height)
                / self.content,
                1.0
            ),
            0.0
        )

    # ========================================================
    # SCROLLING
    # ========================================================

    def apply_offset(self, offset):
        """
        Menetapkan offset baru dengan batas atas/bawah.
        """

        self.offset = max(
            min(offset, self.max_offset()),
            0
        )

        self.place_body()

        if self.scrollbar.winfo_ismapped():

            self.scrollbar.set(
                self.first(),
                self.last()
            )

    def scroll_pixels(self, pixels):
        """
        Menggeser isi sebesar ``pixels``.
        """

        self.apply_offset(
            self.offset + pixels
        )

    def scroll(self, *args):
        """
        Menangani perintah dari scrollbar:
        moveto / scroll / fraction / pageno.
        """

        if not args:

            return

        action = args[0]

        if action == "moveto":

            self.apply_offset(
                max(
                    min(float(args[1]), 1.0),
                    0.0
                ) * self.content
            )

        elif action == "scroll":

            units = (
                args[2]
                if len(args) > 2
                else "units"
            )

            self.scroll_pixels(
                float(args[1])
                * _step_for(
                    units,
                    self.viewport_height
                )
            )

        elif action == "fraction":

            self.apply_offset(
                self.max_offset()
                * max(
                    min(float(args[1]), 1.0),
                    0.0
                )
            )

        elif action == "pageno":

            self.scroll_pixels(
                float(args[1]) * self.viewport_height
            )

    # ========================================================
    # MOUSE WHEEL
    # ========================================================

    def _enter(self, event=None):
        """
        Mengaktifkan scroll wheel saat kursor masuk area.
        """

        self._wheel_depth += 1

        if self._wheel_depth == 1:

            self.bind_all(
                "<MouseWheel>",
                self._on_wheel
            )

            self.bind_all(
                "<Button-4>",
                self._on_wheel_linux
            )

            self.bind_all(
                "<Button-5>",
                self._on_wheel_linux
            )

    def _leave(self, event=None):
        """
        Menonaktifkan scroll wheel saat kursor keluar.
        """

        self._wheel_depth = max(
            self._wheel_depth - 1,
            0
        )

        if self._wheel_depth == 0:

            self.unbind_all("<MouseWheel>")
            self.unbind_all("<Button-4>")
            self.unbind_all("<Button-5>")

    def _on_wheel(self, event):
        """
        Scroll wheel dan two-finger trackpad on Windows/macOS.

        Traditional wheel notches use delta=120; precision
        trackpads report smaller deltas, which are scaled
        proportionally to keep scrolling smooth.
        """

        delta = event.delta

        if not delta:

            return "break"

        scale = WHEEL_STEP / 120 if abs(delta) >= 120 else 1.2

        self.scroll_pixels(-delta * scale)

        return "break"

    def _on_wheel_linux(self, event):
        """
        Scroll wheel untuk Linux (tombol 4 dan 5).
        """

        self.scroll_pixels(
            WHEEL_STEP
            if event.num == 5
            else -WHEEL_STEP
        )

        return "break"
