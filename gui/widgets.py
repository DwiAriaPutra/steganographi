"""
Widget ttk yang sering dipakai ulang.

Tujuan: setiap tab hanya menulis struktur layout-nya,
tidak mengulang baris konfigurasi widget.
"""

import os
import tkinter as tk

from tkinter import ttk

from .theme import COLORS, MONO_FAMILY


IMAGE_FILETYPES = [
    ("PNG / BMP", "*.png *.bmp"),
    ("All files", "*.*"),
]

SAVE_FILETYPES = [
    ("PNG", "*.png"),
    ("BMP", "*.bmp"),
]

PREVIEW_MARGIN = 8


def section_label(parent, text):
    """
    Label judul bagian form.
    """

    return ttk.Label(
        parent,
        text=text,
        style="Section.TLabel"
    )


def section_panel(parent, text):
    """Create a bordered instrument bay for a workflow step."""
    return ttk.LabelFrame(parent, text=text.upper(), padding=(12, 10))


def text_block(parent, height):
    """
    Area teks multi-baris.
    """

    return tk.Text(
        parent,
        height=height,
        wrap="word",
        background=COLORS["well"],
        foreground=COLORS["text"],
        insertbackground=COLORS["green"],
        selectbackground=COLORS["green_dark"],
        selectforeground=COLORS["text"],
        highlightthickness=1,
        highlightbackground=COLORS["border"],
        highlightcolor=COLORS["green"],
        relief="flat",
        padx=10,
        pady=9,
        font=(MONO_FAMILY, 10),
    )


def path_row(
    parent,
    browse_command,
    browse_text="Browse"
):
    """
    Baris path gambar: Entry + tombol Browse.

    Returns:
        ttk.Entry
    """

    frame = ttk.Frame(parent)

    frame.pack(
        fill="x",
        pady=(8, 15)
    )

    entry = ttk.Entry(frame)

    entry.pack(
        side="left",
        fill="x",
        expand=True
    )

    button_label = "SAVE AS" if browse_text.lower() == "save as" else "BROWSE"
    ttk.Button(
        frame,
        text=button_label,
        command=browse_command
    ).pack(
        side="left",
        padx=(8, 0)
    )

    return entry


def secret_entry(parent):
    """
    Entry password (isi disembunyikan).
    """

    entry = ttk.Entry(
        parent,
        show="*"
    )

    entry.pack(
        fill="x",
        pady=(8, 15)
    )

    return entry


def label_frame(
    parent,
    text,
    padding=10,
    height=None
):
    """
    Frame berlabel untuk kelompok widget.

    ``height`` dipakai untuk menjaga tinggi minimum area
    gambar, supaya layout tidak runtuh saat jendela kecil.

    Catatan: opsi ``height`` pada frame yang sudah punya anak
    diabaikan oleh Tk, jadi propagasi ukuran dimatikan agar
    tinggi yang diminta benar-benar dipakai. Anak frame ini
    dipack, maka yang dimatikan adalah ``pack_propagate``.
    """

    frame = ttk.LabelFrame(
        parent,
        text=text,
        padding=padding,
        height=height or 0
    )

    if height:

        frame.pack_propagate(False)

    return frame


def set_entry(entry, value):
    """
    Mengganti isi Entry.
    """

    entry.delete(0, tk.END)

    entry.insert(0, value)


def get_entry(entry, strip=True):
    """
    Membaca isi Entry.
    """

    value = entry.get()

    return value.strip() if strip else value


def get_text(widget, strip_newline=True):
    """
    Membaca isi widget Text.
    """

    value = widget.get("1.0", tk.END)

    return value.rstrip("\n") if strip_newline else value


def set_text(widget, value):
    """
    Mengganti isi widget Text secara aman
    (read-only saat ini).
    """

    widget.config(state="normal")

    widget.delete("1.0", tk.END)

    widget.insert("1.0", value)

    widget.config(state="disabled")


def existing_file(path):
    """
    True bila path terisi dan benar-benar ada di disk.
    """

    return bool(path) and os.path.exists(path)
