"""Lightweight tests for the desktop presentation layer."""

# pylint: disable=import-outside-toplevel

from pathlib import Path

import pytest

from software_fj_reservation_system.domain.client import Client
from software_fj_reservation_system.infrastructure.file_logger import FileLogger
from software_fj_reservation_system.presentation.controller import (
    ReservationSystemController,
)
from software_fj_reservation_system.presentation import controller as presentation_controller
from software_fj_reservation_system.presentation.desktop_app import (
    ReservationDesktopApp,
)


def test_presentation_package_imports() -> None:
    """The presentation package should expose the desktop app and controller."""

    assert ReservationDesktopApp is not None
    assert ReservationSystemController is not None


def test_controller_delegates_client_registration_to_use_case(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """The controller should delegate registration to the application use case."""

    captured: dict[str, object] = {}

    def fake_register_client(repository, logger, payload):  # type: ignore[no-untyped-def]
        captured["repository"] = repository
        captured["logger"] = logger
        captured["payload"] = payload
        return Client(
            id="client-ui-001",
            name="Ana",
            email="ana@softwarefj.com",
            phone="3001234567",
        )

    monkeypatch.setattr(
        presentation_controller,
        "register_client",
        fake_register_client,
    )
    controller = ReservationSystemController(
        logger=FileLogger(log_path=tmp_path / "logs" / "system.log")
    )

    client = controller.register_client("Ana", "ana@softwarefj.com", "3001234567")
    controller.close()

    assert client.id == "client-ui-001"
    assert captured["repository"] is controller.client_repository
    assert captured["logger"] is controller.logger
    assert captured["payload"] == {
        "name": "Ana",
        "email": "ana@softwarefj.com",
        "phone": "3001234567",
    }


def test_desktop_app_supports_root_injection(tmp_path: Path) -> None:
    """The desktop app should allow an injected root for lightweight tests."""

    try:
        import tkinter as tk
    except ImportError:
        pytest.skip("Tkinter is not available in this environment.")

    try:
        root = tk.Tk()
    except tk.TclError:
        pytest.skip("Tk is not available in this environment.")

    root.withdraw()
    controller = ReservationSystemController(
        logger=FileLogger(log_path=tmp_path / "logs" / "system.log")
    )
    app = None

    try:
        app = ReservationDesktopApp(root=root, controller=controller)
        assert app.root is root
    finally:
        if app is not None:
            app.on_close()
        else:
            controller.close()
            root.destroy()
