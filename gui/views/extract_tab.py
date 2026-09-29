"""
Tab Extract.

Menggabili pesan dari stego image memakai stego key.
"""

from tkinter import (
    ttk,
    filedialog,
    messagebox,
)

from steg import extract_message

from ..scroll import ScrollableFrame

from ..widgets import (
    IMAGE_FILETYPES,
    section_panel,
    text_block,
    path_row,
    secret_entry,
    set_entry,
    get_entry,
    set_text,
    existing_file,
)


RESULT_HEIGHT = 12

BUTTON_TEXT = "RECOVER MESSAGE  /  EXTRACT"

VALIDATION_TITLE = "Input belum lengkap"

FAILURE_HINT = (
    "Pesan tidak dapat diekstrak.\n\n"
    "Kemungkinan penyebab:\n"
    "• Stego key salah\n"
    "• Gambar bukan stego image\n"
    "• Data steganografi rusak\n"
    "• Gambar telah dikompresi"
)


class ExtractTab(ttk.Frame):
    """
    Form extract message.
    """

    def __init__(self, master):

        super().__init__(master)

        self.build()

    def build(self):
        """
        Membangun layout form extract.
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

        image_panel = section_panel(form, "01  /  STEGO IMAGE")
        image_panel.pack(fill="x", pady=(0, 10))

        self.image_entry = path_row(
            image_panel,
            self.browse_image
        )

        key_panel = section_panel(form, "02  /  STEGO KEY")
        key_panel.pack(fill="x", pady=(0, 10))

        self.key_entry = secret_entry(key_panel)

        ttk.Button(
            form,
            text=BUTTON_TEXT,
            style="Big.TButton",
            command=self.run_extract
        ).pack(pady=(0, 20))

        result_panel = section_panel(form, "03  /  RECOVERED MESSAGE")
        result_panel.pack(fill="both", expand=True)

        self.result_text = text_block(
            result_panel,
            RESULT_HEIGHT
        )

        self.result_text.pack(
            fill="both",
            expand=True,
            pady=(2, 0)
        )

        self.result_text.config(
            state="disabled"
        )

    def browse_image(self):
        """
        Memilih stego image.
        """

        path = filedialog.askopenfilename(
            title="Pilih Stego Image",
            filetypes=IMAGE_FILETYPES
        )

        if not path:

            return

        set_entry(
            self.image_entry,
            path
        )

    def collect_input(self):
        """
        Membaca dan memvalidasi field form.

        Returns:
            tuple | None
        """

        image = get_entry(self.image_entry)

        key = get_entry(
            self.key_entry,
            strip=False
        )

        if not image or not existing_file(image):

            messagebox.showwarning(
                VALIDATION_TITLE,
                "Pilih stego image."
            )

            return None

        if not key:

            messagebox.showwarning(
                VALIDATION_TITLE,
                "Masukkan stego key."
            )

            return None

        return image, key

    def run_extract(self):
        """
        Menjalankan extract dan menampilkan hasilnya.
        """

        values = self.collect_input()

        if values is None:

            return

        image, key = values

        try:

            result = extract_message(image, key)

        except Exception:

            messagebox.showerror(
                "Extract gagal",
                FAILURE_HINT
            )

            return

        set_text(
            self.result_text,
            result["message"]
        )

        messagebox.showinfo(
            "Extract berhasil",
            "Pesan berhasil diekstrak."
        )
