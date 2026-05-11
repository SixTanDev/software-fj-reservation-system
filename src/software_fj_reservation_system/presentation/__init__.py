"""Desktop presentation layer for the Software FJ reservation system."""

from __future__ import annotations

# pylint: disable=import-outside-toplevel

from typing import TYPE_CHECKING, Any

from software_fj_reservation_system.presentation.controller import (
    ReservationSystemController,
)

if TYPE_CHECKING:
    from software_fj_reservation_system.presentation.desktop_app import ReservationDesktopApp

__all__ = ["ReservationDesktopApp", "ReservationSystemController"]


def __getattr__(name: str) -> Any:
    """Lazily expose the Tkinter app without preloading the executable module."""

    if name == "ReservationDesktopApp":
        from software_fj_reservation_system.presentation.desktop_app import (
            ReservationDesktopApp,
        )

        return ReservationDesktopApp
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
