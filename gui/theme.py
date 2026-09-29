"""Shared industrial terminal theme for the Tkinter interface."""

import tkinter as tk
from tkinter import ttk


FONT_FAMILY = "Georgia"
MONO_FAMILY = "Consolas"
THEME = "clam"

COLORS = {
    "background": "#ede7da",
    "surface": "#f6f3ea",
    "panel": "#fcfaf6",
    "raised": "#e8e0d1",
    "well": "#fbf9f5",
    "border": "#d6cdbe",
    "border_active": "#b8ac99",
    "text": "#222421",
    "muted": "#5a5e56",
    "green": "#243b2f",
    "green_dark": "#1c2f25",
    "amber": "#c29758",
    "cyan": "#3d443f",
    "red": "#c95f54",
}

TITLE_FONT = (FONT_FAMILY, 12, "bold")
EMPTY_TEXT = "BELUM ADA DATA"
CANVAS_BG = COLORS["well"]
IMAGE_BG = COLORS["well"]
IMAGE_PLACEHOLDER_COLOR = COLORS["muted"]
GRID_COLOR = COLORS["border"]
AXIS_COLOR = COLORS["muted"]
PLACEHOLDER_TEXT = "BELUM ADA GAMBAR"


def apply_style(root):
    """Apply a consistent dark terminal palette to ttk and Tk widgets."""
    root.configure(background=COLORS["background"])
    style = ttk.Style(root)
    try:
        style.theme_use(THEME)
    except tk.TclError:
        pass

    base = COLORS["surface"]
    text = COLORS["text"]
    muted = COLORS["muted"]
    border = COLORS["border"]
    raised = COLORS["raised"]
    green = COLORS["green"]

    style.configure(".", background=base, foreground=text, font=("Segoe UI", 10))
    style.configure("TFrame", background=base)
    style.configure("TLabel", background=base, foreground=text)
    style.configure("Muted.TLabel", foreground=muted, font=(MONO_FAMILY, 9))
    style.configure("Eyebrow.TLabel", foreground=muted, background=base, font=(MONO_FAMILY, 9, "bold"))
    style.configure("Title.TLabel", background=base, foreground=text, font=("Georgia", 30, "normal"))
    style.configure("Subtitle.TLabel", background=base, foreground=muted, font=("Segoe UI", 10))
    style.configure("Section.TLabel", background=base, foreground=text, font=("Georgia", 15, "bold"))
    style.configure("Metric.TLabel", background=base, foreground=green, font=(MONO_FAMILY, 18, "bold"))
    style.configure("Big.TButton", font=(MONO_FAMILY, 10, "bold"), padding=(14, 10), background=green, foreground="#ffffff", bordercolor=green, lightcolor=green, darkcolor=green)
    style.map("Big.TButton", background=[("disabled", raised), ("pressed", "#1c2f25"), ("active", "#2f4b3c")], foreground=[("disabled", muted), ("!disabled", "#ffffff")])
    style.configure("TButton", font=(MONO_FAMILY, 9, "bold"), padding=(10, 7), background=raised, foreground=text, bordercolor=border, lightcolor=COLORS["panel"], darkcolor=COLORS["border_active"])
    style.map("TButton", background=[("pressed", "#d8cfbf"), ("active", "#f1ecdf")], foreground=[("active", green)])
    style.configure("TEntry", fieldbackground=COLORS["well"], foreground=text, insertcolor=green, bordercolor=border, lightcolor=border, darkcolor=border, padding=8)
    style.map("TEntry", bordercolor=[("focus", green)])
    style.configure("TNotebook", background=raised, bordercolor=border, tabmargins=(0, 5, 4, 0))
    style.configure("TNotebook.Tab", background=raised, foreground=muted, padding=(15, 9), font=(MONO_FAMILY, 9, "bold"), bordercolor=border)
    style.map("TNotebook.Tab", background=[("selected", COLORS["surface"]), ("active", COLORS["panel"])], foreground=[("selected", text), ("active", green)])
    style.configure("TLabelframe", background=COLORS["panel"], bordercolor=border, relief="solid")
    style.configure("TLabelframe.Label", background=COLORS["panel"], foreground=text, font=("Georgia", 14, "bold"))
    style.configure("TScrollbar", background=raised, troughcolor=COLORS["surface"], bordercolor=base, arrowcolor=muted)
    style.configure("Horizontal.TProgressbar", background=green, troughcolor=COLORS["well"], bordercolor=border)

    return style
