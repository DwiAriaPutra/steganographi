"""
Shell aplikasi GUI.

``SteganographyApp`` hanya merakit potongan-potongan:
header, notebook utama, dan tiga tab. Logika domain tetap
di paket ``steg`` dan ``analysis``.
"""

import tkinter as tk

from tkinter import (
    ttk,
    messagebox,
)

from .session import Session

from .theme import COLORS, apply_style

from .views.embed_tab import EmbedTab

from .views.extract_tab import ExtractTab

from .views.analysis_tab import AnalysisTab


TITLE = "Steganography Analyzer"

SUBTITLE = (
    "Image steganography menggunakan LSB + AES-GCM"
)

GEOMETRY = (1100, 760)

SCREEN_RATIO = 0.9

MIN_SIZE = (820, 520)

NOTEBOOK_PADDING = {"padx": 18, "pady": (0, 12)}

TABS = (
    ("Embed", "  Embed  "),
    ("Analysis", "  Analysis  "),
    ("Extract", "  Extract  "),
)


class SteganographyApp(tk.Tk):
    """
    Jendela utama Steganography Analyzer.
    """

    def __init__(self):

        super().__init__()

        self.title(TITLE)

        self.apply_geometry()

        self.minsize(*MIN_SIZE)

        self.session = Session()

        apply_style(self)

        self.create_header()

        self.create_notebook()

        self.create_tabs()

        self.create_footer()

    def apply_geometry(self):
        """
        Menyesuaikan ukuran jendela dengan layar monitor
        dan menengahkan jendela.
        """

        screen_width = self.winfo_screenwidth()

        screen_height = self.winfo_screenheight()

        width = min(
            GEOMETRY[0],
            int(screen_width * SCREEN_RATIO)
        )

        height = min(
            GEOMETRY[1],
            int(screen_height * SCREEN_RATIO)
        )

        x = (screen_width - width) // 2

        y = (screen_height - height) // 2

        self.geometry(
            f"{width}x{height}+{x}+{y}"
        )

    def create_header(self):
        """
        Judul aplikasi di bagian atas jendela.
        """

        frame = ttk.Frame(self, padding=(22, 15, 22, 13))

        frame.pack(fill="x")

        brand = ttk.Frame(frame)
        brand.pack(fill="x", pady=(0, 15))

        lights = ttk.Frame(brand)
        lights.pack(side="left", padx=(0, 12))
        for color in (COLORS["red"], COLORS["amber"], COLORS["green"]):
            tk.Label(lights, text=" ", bg=color, width=1, height=0).pack(side="left", padx=(0, 5))

        ttk.Label(
            brand,
            text="INSTRUMENT SPECIMEN  /  AES-GCM + LSB",
            style="Muted.TLabel",
        ).pack(side="left")

        ttk.Label(
            brand,
            text="[SYS.READY] ENGINE READY",
            foreground=COLORS["green"],
            style="Muted.TLabel",
        ).pack(side="right")

        ttk.Separator(frame, orient="horizontal").pack(fill="x", pady=(0, 14))

        heading = ttk.Frame(frame)
        heading.pack(fill="x")

        title_group = ttk.Frame(heading)
        title_group.pack(side="left", fill="x", expand=True)

        ttk.Label(
            title_group,
            text="STEGANOGRAPHIC LABORATORY  /  LOCAL WORKSTATION",
            style="Eyebrow.TLabel",
        ).pack(anchor="w", pady=(0, 3))

        ttk.Label(
            title_group,
            text=TITLE,
            style="Title.TLabel"
        ).pack(anchor="w")

        ttk.Label(
            title_group,
            text=SUBTITLE,
            style="Subtitle.TLabel"
        ).pack(
            anchor="w",
            pady=(3, 0)
        )

        badge = tk.Frame(heading, bg=COLORS["well"], highlightbackground=COLORS["border"], highlightthickness=1, padx=14, pady=10)
        badge.pack(side="right", padx=(16, 0))
        tk.Label(badge, text="CRYPTOGRAPHIC CIPHER", bg=COLORS["well"], fg=COLORS["amber"], font=("Consolas", 8, "bold")).pack()
        tk.Label(badge, text="AES-GCM  /  256-BIT", bg=COLORS["well"], fg=COLORS["green"], font=("Consolas", 10, "bold")).pack(pady=(3, 0))

    def create_notebook(self):
        """
        Notebook utama tempat semua tab dipasang.
        """

        self.notebook = ttk.Notebook(self)

        self.notebook.pack(
            fill="both",
            expand=True,
            **NOTEBOOK_PADDING
        )

        self.frames = {
            name: ttk.Frame(self.notebook)
            for name, _ in TABS
        }

        for name, label in TABS:

            self.notebook.add(
                self.frames[name],
                text=label
            )

    def create_footer(self):
        """Show the active cipher and local session state."""
        footer = ttk.Frame(self, padding=(18, 8))
        footer.pack(fill="x", side="bottom")
        ttk.Separator(footer, orient="horizontal").pack(fill="x", pady=(0, 7))
        ttk.Label(footer, text="CIPHER: AES/GCM  /  EMBED: SPATIAL 1-LSB", style="Muted.TLabel").pack(side="left")
        ttk.Label(footer, text="SESSION: LOCAL MACHINE   /   READY", foreground=COLORS["green"], style="Muted.TLabel").pack(side="right")

    def create_tabs(self):
        """
        Membuat isi tiap tab.
        """

        self.embed_tab = EmbedTab(
            self.frames["Embed"],
            self.session,
            on_embedded=self.on_embedded
        )

        self.analysis_tab = AnalysisTab(
            self.frames["Analysis"],
            self.session,
            on_error=self.show_error,
            on_lsb_error=self.show_lsb_error
        )

        self.extract_tab = ExtractTab(
            self.frames["Extract"]
        )

        for tab in (
            self.embed_tab,
            self.analysis_tab,
            self.extract_tab
        ):

            tab.pack(
                fill="both",
                expand=True
            )

    def on_embedded(self):
        """
        Dipanggil tab embed setelah embed berhasil.

        Muat ulang analisis lalu arahkan user ke tab Analysis.
        """

        self.analysis_tab.refresh()

        self.notebook.select(
            self.frames["Analysis"]
        )

    def show_error(
        self,
        error,
        title="Analysis gagal"
    ):
        """
        Menampilkan error ke user sebagai dialog.
        """

        messagebox.showerror(
            title,
            str(error)
        )

    def show_lsb_error(self, error):
        """
        Dialog khusus untuk kegagalan LSB analysis.
        """

        self.show_error(
            error,
            "LSB Analysis gagal"
        )

    def run(self):
        """
        Menjalankan event loop Tk.
        """

        self.mainloop()
