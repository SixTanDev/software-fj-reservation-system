"""Shared ttk styles for the desktop presentation layer."""

from __future__ import annotations

# pylint: disable=import-outside-toplevel

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import tkinter as tk
    from tkinter import ttk

PALETTE = {
    "background": "#0F172A",
    "surface": "#111827",
    "surface_alt": "#1E293B",
    "text": "#F8FAFC",
    "text_muted": "#CBD5E1",
    "primary": "#2563EB",
    "primary_hover": "#1D4ED8",
    "success": "#16A34A",
    "error": "#DC2626",
    "warning": "#F59E0B",
    "border": "#334155",
}


def configure_styles(root: tk.Misc) -> ttk.Style:
    """Configure a cohesive themed ttk style set for the desktop app."""

    from tkinter import ttk

    style = ttk.Style(root)
    if "clam" in style.theme_names():
        style.theme_use("clam")

    root.configure(background=PALETTE["background"])

    style.configure("App.TFrame", background=PALETTE["background"])
    style.configure("Surface.TFrame", background=PALETTE["surface"])
    style.configure(
        "Card.TFrame",
        background=PALETTE["surface"],
        borderwidth=1,
        relief="solid",
    )
    style.configure(
        "Panel.TLabelframe",
        background=PALETTE["surface"],
        borderwidth=1,
        relief="solid",
    )
    style.configure(
        "Panel.TLabelframe.Label",
        background=PALETTE["surface"],
        foreground=PALETTE["text"],
        font=("Helvetica", 11, "bold"),
    )
    style.configure(
        "TLabel",
        background=PALETTE["background"],
        foreground=PALETTE["text"],
        font=("Helvetica", 10),
    )
    style.configure(
        "Title.TLabel",
        background=PALETTE["surface"],
        foreground=PALETTE["text"],
        font=("Helvetica", 22, "bold"),
    )
    style.configure(
        "Subtitle.TLabel",
        background=PALETTE["surface"],
        foreground=PALETTE["text_muted"],
        font=("Helvetica", 11),
    )
    style.configure(
        "Section.TLabel",
        background=PALETTE["surface"],
        foreground=PALETTE["text_muted"],
        font=("Helvetica", 10, "bold"),
    )
    style.configure(
        "Metric.TLabel",
        background=PALETTE["surface"],
        foreground=PALETTE["text"],
        font=("Helvetica", 26, "bold"),
    )
    style.configure(
        "Body.TLabel",
        background=PALETTE["surface"],
        foreground=PALETTE["text"],
        font=("Helvetica", 10),
    )
    style.configure(
        "Muted.TLabel",
        background=PALETTE["surface"],
        foreground=PALETTE["text_muted"],
        font=("Helvetica", 10),
    )
    style.configure(
        "Status.TLabel",
        background=PALETTE["surface_alt"],
        foreground=PALETTE["text"],
        font=("Helvetica", 10, "bold"),
        padding=(14, 10),
    )

    common_field_config = {
        "fieldbackground": PALETTE["surface_alt"],
        "background": PALETTE["surface_alt"],
        "foreground": PALETTE["text"],
        "padding": 8,
    }
    style.configure("TEntry", **common_field_config)
    style.configure("TCombobox", **common_field_config)
    style.map(
        "TCombobox",
        fieldbackground=[("readonly", PALETTE["surface_alt"])],
        foreground=[("readonly", PALETTE["text"])],
        selectbackground=[("readonly", PALETTE["primary"])],
    )

    style.configure(
        "TNotebook",
        background=PALETTE["background"],
        borderwidth=0,
        tabmargins=(0, 0, 0, 0),
    )
    style.configure(
        "TNotebook.Tab",
        background=PALETTE["surface_alt"],
        foreground=PALETTE["text_muted"],
        padding=(18, 10),
        font=("Helvetica", 10, "bold"),
    )
    style.map(
        "TNotebook.Tab",
        background=[("selected", PALETTE["primary"]), ("active", PALETTE["surface"])],
        foreground=[("selected", PALETTE["text"]), ("active", PALETTE["text"])],
    )

    style.configure(
        "Primary.TButton",
        background=PALETTE["primary"],
        foreground=PALETTE["text"],
        borderwidth=0,
        padding=(14, 9),
        font=("Helvetica", 10, "bold"),
    )
    style.map(
        "Primary.TButton",
        background=[("active", PALETTE["primary_hover"]), ("disabled", PALETTE["border"])],
        foreground=[("disabled", PALETTE["text_muted"])],
    )
    style.configure(
        "Secondary.TButton",
        background=PALETTE["surface_alt"],
        foreground=PALETTE["text"],
        borderwidth=0,
        padding=(14, 9),
        font=("Helvetica", 10, "bold"),
    )
    style.map(
        "Secondary.TButton",
        background=[("active", PALETTE["surface"]), ("disabled", PALETTE["border"])],
        foreground=[("disabled", PALETTE["text_muted"])],
    )

    style.configure(
        "Treeview",
        background=PALETTE["surface"],
        fieldbackground=PALETTE["surface"],
        foreground=PALETTE["text"],
        rowheight=28,
    )
    style.configure(
        "Treeview.Heading",
        background=PALETTE["surface_alt"],
        foreground=PALETTE["text"],
        borderwidth=0,
        font=("Helvetica", 10, "bold"),
        padding=(8, 8),
    )
    style.map(
        "Treeview",
        background=[("selected", PALETTE["primary"])],
        foreground=[("selected", PALETTE["text"])],
    )
    return style
