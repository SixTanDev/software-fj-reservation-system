"""Baseline tests for the repository scaffold."""

from importlib.metadata import version

import software_fj_reservation_system


def test_baseline_package_is_installable() -> None:
    """Verify that uv, packaging, and pytest are wired before domain code exists."""
    # This smoke test is intentionally small until the real client, service, and reservation
    # modules are created in later implementation tasks.
    assert software_fj_reservation_system.__doc__
    assert version("software-fj-reservation-system") == "0.1.0"
