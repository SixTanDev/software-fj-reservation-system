"""Shared ttk styles for the desktop presentation layer."""

from __future__ import annotations

# pylint: disable=import-outside-toplevel

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import tkinter as tk
    from tkinter import ttk

PALETTE = {
    "background": "#071224",
    "surface": "#0E1A2B",
    "surface_alt": "#132238",
    "table_header": "#1E2B3F",
    "border": "#2A3A55",
    "text": "#F8FAFC",
    "text_muted": "#B6C2D1",
    "primary": "#3B82F6",
    "primary_hover": "#2563EB",
    "success": "#22C55E",
    "success_hover": "#16A34A",
    "error": "#EF4444",
    "error_hover": "#DC2626",
    "warning": "#F59E0B",
    "row_alt": "#101F34",
}

SPACING = {
    "page": 24,
    "panel": 18,
    "section": 16,
    "field": 12,
    "label": 8,
}

FONT_FAMILY = "Helvetica"
MONOSPACE_FONT = ("Menlo", 10)


def configure_styles(root: tk.Misc) -> ttk.Style:
    """Configure a cohesive themed ttk style set for the desktop app."""

    from tkinter import ttk

    style = ttk.Style(root)
    if "clam" in style.theme_names():
        style.theme_use("clam")

    root.configure(background=PALETTE["background"])
    root.option_add("*TCombobox*Listbox.background", PALETTE["surface_alt"])
    root.option_add("*TCombobox*Listbox.foreground", PALETTE["text"])
    root.option_add("*TCombobox*Listbox.selectBackground", PALETTE["primary"])
    root.option_add("*TCombobox*Listbox.selectForeground", PALETTE["text"])

    style.configure("App.TFrame", background=PALETTE["background"])
    style.configure("Surface.TFrame", background=PALETTE["surface"])
    style.configure(
        "Card.TFrame",
        background=PALETTE["surface"],
        bordercolor=PALETTE["border"],
        borderwidth=1,
        relief="solid",
    )
    style.configure(
        "Panel.TLabelframe",
        background=PALETTE["surface"],
        bordercolor=PALETTE["border"],
        darkcolor=PALETTE["border"],
        lightcolor=PALETTE["border"],
        borderwidth=1,
        relief="solid",
    )
    style.configure(
        "Panel.TLabelframe.Label",
        background=PALETTE["surface"],
        foreground=PALETTE["text"],
        font=(FONT_FAMILY, 11, "bold"),
        padding=(0, 0, 0, 4),
    )
    style.configure(
        "TLabel",
        background=PALETTE["background"],
        foreground=PALETTE["text"],
        font=(FONT_FAMILY, 10),
    )
    style.configure(
        "Title.TLabel",
        background=PALETTE["surface"],
        foreground=PALETTE["text"],
        font=(FONT_FAMILY, 23, "bold"),
    )
    style.configure(
        "Subtitle.TLabel",
        background=PALETTE["surface"],
        foreground=PALETTE["text_muted"],
        font=(FONT_FAMILY, 11),
    )
    style.configure(
        "Section.TLabel",
        background=PALETTE["surface"],
        foreground=PALETTE["text_muted"],
        font=(FONT_FAMILY, 10, "bold"),
    )
    style.configure(
        "CardTitle.TLabel",
        background=PALETTE["surface"],
        foreground=PALETTE["text_muted"],
        font=(FONT_FAMILY, 10, "bold"),
    )
    style.configure(
        "Metric.TLabel",
        background=PALETTE["surface"],
        foreground=PALETTE["text"],
        font=(FONT_FAMILY, 27, "bold"),
    )
    style.configure(
        "Body.TLabel",
        background=PALETTE["surface"],
        foreground=PALETTE["text"],
        font=(FONT_FAMILY, 10),
    )
    style.configure(
        "Muted.TLabel",
        background=PALETTE["surface"],
        foreground=PALETTE["text_muted"],
        font=(FONT_FAMILY, 10),
    )
    style.configure(
        "AppMuted.TLabel",
        background=PALETTE["background"],
        foreground=PALETTE["text_muted"],
        font=(FONT_FAMILY, 9),
    )
    style.configure(
        "Empty.TLabel",
        background=PALETTE["surface"],
        foreground=PALETTE["text_muted"],
        font=(FONT_FAMILY, 11),
        padding=(18, 18),
    )
    style.configure(
        "Selection.TLabel",
        background=PALETTE["surface_alt"],
        foreground=PALETTE["text_muted"],
        font=(FONT_FAMILY, 10),
        padding=(12, 10),
    )
    style.configure(
        "Status.TLabel",
        background=PALETTE["surface_alt"],
        foreground=PALETTE["text"],
        font=(FONT_FAMILY, 10, "bold"),
        padding=(14, 10),
    )

    common_field_config = {
        "fieldbackground": PALETTE["surface_alt"],
        "background": PALETTE["surface_alt"],
        "foreground": PALETTE["text"],
        "bordercolor": PALETTE["border"],
        "lightcolor": PALETTE["border"],
        "darkcolor": PALETTE["border"],
        "insertcolor": PALETTE["text"],
        "padding": (10, 9),
        "font": (FONT_FAMILY, 10),
    }
    style.configure("TEntry", **common_field_config)
    style.configure("TCombobox", **common_field_config)
    style.map(
        "TEntry",
        fieldbackground=[
            ("focus", PALETTE["surface_alt"]),
            ("disabled", PALETTE["surface"]),
        ],
        bordercolor=[("focus", PALETTE["primary"])],
        foreground=[("disabled", PALETTE["text_muted"])],
    )
    style.map(
        "TCombobox",
        fieldbackground=[("readonly", PALETTE["surface_alt"])],
        foreground=[("readonly", PALETTE["text"])],
        selectbackground=[("readonly", PALETTE["primary"])],
        bordercolor=[("focus", PALETTE["primary"])],
        arrowcolor=[("active", PALETTE["text"]), ("readonly", PALETTE["text_muted"])],
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
        borderwidth=0,
        padding=(20, 11),
        font=(FONT_FAMILY, 10, "bold"),
    )
    style.map(
        "TNotebook.Tab",
        background=[
            ("selected", PALETTE["primary"]),
            ("active", PALETTE["table_header"]),
        ],
        foreground=[("selected", PALETTE["text"]), ("active", PALETTE["text"])],
    )

    style.configure(
        "Primary.TButton",
        background=PALETTE["primary"],
        foreground=PALETTE["text"],
        borderwidth=0,
        focuscolor=PALETTE["primary"],
        padding=(14, 10),
        font=(FONT_FAMILY, 10, "bold"),
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
        focuscolor=PALETTE["surface_alt"],
        padding=(14, 10),
        font=(FONT_FAMILY, 10, "bold"),
    )
    style.map(
        "Secondary.TButton",
        background=[("active", PALETTE["table_header"]), ("disabled", PALETTE["border"])],
        foreground=[("disabled", PALETTE["text_muted"])],
    )
    style.configure(
        "Success.TButton",
        background=PALETTE["success"],
        foreground=PALETTE["background"],
        borderwidth=0,
        focuscolor=PALETTE["success"],
        padding=(14, 10),
        font=(FONT_FAMILY, 10, "bold"),
    )
    style.map(
        "Success.TButton",
        background=[("active", PALETTE["success_hover"]), ("disabled", PALETTE["border"])],
        foreground=[("disabled", PALETTE["text_muted"])],
    )
    style.configure(
        "Danger.TButton",
        background=PALETTE["error"],
        foreground=PALETTE["text"],
        borderwidth=0,
        focuscolor=PALETTE["error"],
        padding=(14, 10),
        font=(FONT_FAMILY, 10, "bold"),
    )
    style.map(
        "Danger.TButton",
        background=[("active", PALETTE["error_hover"]), ("disabled", PALETTE["border"])],
        foreground=[("disabled", PALETTE["text_muted"])],
    )

    style.configure(
        "Treeview",
        background=PALETTE["surface"],
        fieldbackground=PALETTE["surface"],
        foreground=PALETTE["text"],
        bordercolor=PALETTE["border"],
        borderwidth=0,
        font=(FONT_FAMILY, 10),
        rowheight=32,
    )
    style.configure(
        "Treeview.Heading",
        background=PALETTE["table_header"],
        foreground=PALETTE["text"],
        relief="flat",
        borderwidth=0,
        font=(FONT_FAMILY, 10, "bold"),
        padding=(10, 9),
    )
    style.map(
        "Treeview",
        background=[("selected", PALETTE["primary"])],
        foreground=[("selected", PALETTE["text"])],
    )
    style.configure(
        "Vertical.TScrollbar",
        background=PALETTE["surface_alt"],
        bordercolor=PALETTE["surface"],
        arrowcolor=PALETTE["text_muted"],
        troughcolor=PALETTE["surface"],
        relief="flat",
        width=12,
    )
    style.map(
        "Vertical.TScrollbar",
        background=[("active", PALETTE["table_header"])],
        arrowcolor=[("active", PALETTE["text"])],
    )
    style.configure(
        "Horizontal.TScrollbar",
        background=PALETTE["surface_alt"],
        bordercolor=PALETTE["surface"],
        arrowcolor=PALETTE["text_muted"],
        troughcolor=PALETTE["surface"],
        relief="flat",
        width=12,
    )
    style.map(
        "Horizontal.TScrollbar",
        background=[("active", PALETTE["table_header"])],
        arrowcolor=[("active", PALETTE["text"])],
    )
    return style
