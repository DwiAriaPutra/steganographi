"""
Tab Embed.

Alur: pilih cover image -> tulis pesan -> masukkan key ->
tentukan output -> embed. Setelah berhasil, tab analisis
dimuat ulang otomatis.
"""

import tkinter as tk

from tkinter import (
    ttk,
    filedialog,
    messagebox,
)

from PIL import Image, ImageTk

from steg import (
    embed_message,
    get_capacity,
)

from ..scroll import ScrollableFrame

from ..widgets import (
    IMAGE_FILETYPES,
    SAVE_FILETYPES,
    section_panel,
    text_block,
    path_row,
    set_entry,
    get_entry,
    get_text,
    existing_file,
)

from ..theme import COLORS, MONO_FAMILY


MESSAGE_HEIGHT = 8

BUTTON_TEXT = "INJECT MESSAGE  /  EMBED"

CAPACITY_PLACEHOLDER = "Kapasitas: belum ada gambar"

VALIDATION_TITLE = "Input belum lengkap"

VALIDATION = {
    "cover": "Pilih cover image terlebih dahulu.",
    "output": "Tentukan output stego image.",
    "message": "Masukkan pesan.",
    "key": "Masukkan stego key.",
}


class EmbedTab(ttk.Frame):
    """
    Form embed message.
    """

    def __init__(
        self,
        master,
        session,
        on_embedded=None
    ):

        super().__init__(master)

        self.session = session

        self.on_embedded = on_embedded

        self.build()

    def build(self):
        """
        Membangun layout form embed.
        """

        self.scroller = ScrollableFrame(
            self,
            padding=20
        )

        self.scroller.pack(
            fill="both",
            expand=True
        )

        form = self.scroller.body
        form.columnconfigure(0, weight=6, uniform="embed")
        form.columnconfigure(1, weight=4, uniform="embed")
        form.rowconfigure(0, weight=1)

        left = ttk.Frame(form)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        right = ttk.Frame(form)
        right.grid(row=0, column=1, sticky="nsew", padx=(0, 1))

        cover_panel = section_panel(left, "1  Cover Image")
        cover_panel.pack(fill="x", pady=(0, 12))
        self.cover_entry = path_row(cover_panel, self.browse_cover)
        self.preview_label = tk.Label(
            cover_panel,
            text="PILIH GAMBAR CARRIER UNTUK PREVIEW",
            background="#111311",
            foreground="#d6cdbe",
            font=(MONO_FAMILY, 9),
            height=10,
            relief="flat",
            anchor="center",
        )
        self.preview_label.pack(fill="x", pady=(0, 9))
        self.capacity_label = ttk.Label(
            cover_panel,
            text=CAPACITY_PLACEHOLDER,
            style="Muted.TLabel",
            wraplength=700,
        )
        self.capacity_label.pack(anchor="w", pady=(0, 2))

        message_panel = section_panel(left, "2  Secret Message")
        message_panel.pack(fill="both", expand=True)
        self.message_text = text_block(message_panel, MESSAGE_HEIGHT)
        self.message_text.pack(fill="both", expand=True, pady=(1, 7))
        ttk.Label(
            message_panel,
            text="Pesan dienkripsi dengan AES-256-GCM sebelum disisipkan ke bit LSB gambar.",
            style="Muted.TLabel",
            wraplength=680,
        ).pack(anchor="w", pady=(0, 2))

        key_panel = section_panel(right, "3  Stego Key")
        key_panel.pack(fill="x", pady=(0, 12))
        ttk.Label(key_panel, text="Kunci enkripsi AES-256 (GCM mode)", style="Muted.TLabel").pack(anchor="w", pady=(0, 5))
        key_row = ttk.Frame(key_panel)
        key_row.pack(fill="x", pady=(0, 8))
        self.key_entry = ttk.Entry(key_row, show="*")
        self.key_entry.pack(side="left", fill="x", expand=True)
        self.key_visible = False
        self.key_visibility_button = ttk.Button(
            key_row,
            text="SHOW",
            command=self.toggle_key_visibility,
        )
        self.key_visibility_button.pack(side="left", padx=(7, 0))
        ttk.Label(key_panel, text="Kunci yang sama diperlukan saat ekstraksi.", style="Muted.TLabel").pack(anchor="w", pady=(0, 2))

        output_panel = section_panel(right, "4  Output Stego Image")
        output_panel.pack(fill="x", pady=(0, 12))
        self.output_entry = path_row(output_panel, self.browse_output, browse_text="Save As")

        ttk.Button(
            right,
            text=BUTTON_TEXT,
            style="Big.TButton",
            command=self.run_embed,
        ).pack(fill="x", pady=(0, 9))
        self.status_label = ttk.Label(right, text="", style="Muted.TLabel", wraplength=400)
        self.status_label.pack(fill="x", pady=(0, 8))

        spec_panel = section_panel(right, "Cipher Specification")
        spec_panel.pack(fill="x")
        ttk.Label(spec_panel, text="CIPHER SPEC     AES-256 / GCM / TAG", style="Muted.TLabel").pack(anchor="w", pady=(2, 5))
        ttk.Label(spec_panel, text="BIT-PLANE DEPTH     LSB-1  (RGB)", style="Muted.TLabel").pack(anchor="w", pady=(0, 5))
        ttk.Label(spec_panel, text="INTEGRITY CHECK     GCM AUTHENTICATION", style="Muted.TLabel").pack(anchor="w", pady=(0, 2))

    def toggle_key_visibility(self):
        """Toggle visibility of the encryption key field."""
        self.key_visible = not self.key_visible
        self.key_entry.configure(show="" if self.key_visible else "*")
        self.key_visibility_button.configure(text="HIDE" if self.key_visible else "SHOW")

    def browse_cover(self):
        """
        Memilih cover image.
        """

        path = filedialog.askopenfilename(
            title="Pilih Cover Image",
            filetypes=IMAGE_FILETYPES
        )

        if not path:

            return

        set_entry(
            self.cover_entry,
            path
        )

        self.update_capacity()
        self.update_preview(path)

    def update_preview(self, path):
        """Show a scaled thumbnail of the selected carrier image."""
        try:
            self.preview_label.update_idletasks()
            available_width = self.preview_label.winfo_width() - 12
            if available_width < 100:
                available_width = 560
            with Image.open(path) as source:
                width, height = source.size
                preview = source.convert("RGB")
                preview.thumbnail((min(900, available_width), 300))
            self.preview_photo = ImageTk.PhotoImage(preview)
            self.preview_label.config(
                image=self.preview_photo,
                text=f"PREVIEW: {width} x {height} px (RGB)",
                compound="bottom",
                height=0,
            )
        except Exception:
            self.preview_photo = None
            self.preview_label.config(image="", text="PREVIEW TIDAK TERSEDIA", height=10)

    def browse_output(self):
        """
        Memilih path output stego image.
        """

        path = filedialog.asksaveasfilename(
            title="Simpan Stego Image",
            defaultextension=".png",
            filetypes=SAVE_FILETYPES
        )

        if not path:

            return

        set_entry(
            self.output_entry,
            path
        )

    def update_capacity(self):
        """
        Menampilkan kapasitas cover image terpilih.
        """

        path = get_entry(self.cover_entry)

        if not existing_file(path):

            return

        try:

            info = get_capacity(path)

        except Exception as error:

            self.capacity_label.config(
                text=f"Error: {error}"
            )

            return

        self.capacity_label.config(
            text=(
                f"Ukuran: "
                f"{info['width']} × "
                f"{info['height']} px    |    "
                f"Kapasitas: "
                f"{info['capacity_bytes']:,} byte    |    "
                f"Maks. pesan: "
                f"{info['max_message_bytes']:,} byte"
            )
        )

    def collect_input(self):
        """
        Membaca dan memvalidasi seluruh field form.

        Returns:
            tuple | None
        """

        input_image = get_entry(
            self.cover_entry
        )

        output_image = get_entry(
            self.output_entry
        )

        message = get_text(
            self.message_text
        )

        key = get_entry(
            self.key_entry,
            strip=False
        )

        fields = (
            ("cover", input_image),
            ("output", output_image),
            ("message", message),
            ("key", key),
        )

        for name, value in fields:

            if not value:

                messagebox.showwarning(
                    VALIDATION_TITLE,
                    VALIDATION[name]
                )

                return None

        return input_image, output_image, message, key

    def run_embed(self):
        """
        Menjalankan embed dan memuat ulang tab analisis.
        """

        values = self.collect_input()

        if values is None:

            return

        input_image, output_image, message, key = values

        try:

            result = embed_message(
                input_image,
                output_image,
                message,
                key
            )

        except Exception as error:

            messagebox.showerror(
                "Embed gagal",
                str(error)
            )

            return

        self.session.set_pair(
            input_image,
            output_image
        )

        self.status_label.config(
            text=(
                "✓ Stego image berhasil dibuat. "
                f"Pesan: {result['message_bytes']} byte"
            )
        )

        messagebox.showinfo(
            "Embed berhasil",
            (
                "Stego image berhasil dibuat.\n\n"
                f"Output:\n{output_image}"
            )
        )

        if self.on_embedded:

            self.on_embedded()
