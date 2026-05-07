"""Simulation tests for the Software FJ reservation system."""

from pathlib import Path

from software_fj_reservation_system.simulation.operations_simulator import (
    execute_simulation,
)


def test_simulation_executes_minimum_operations_and_generates_logs(
    tmp_path: Path,
    capsys,
) -> None:
    """The simulation should keep running after controlled failures."""

    log_path = tmp_path / "logs" / "system.log"

    results = execute_simulation(log_path=log_path, max_bytes=4096, backup_count=1)

    captured = capsys.readouterr()
    business_operations = [
        entry for entry in results if entry["status"] in {"ok", "error"}
    ]

    assert len(business_operations) >= 12
    assert any(entry["status"] == "error" for entry in results)
    assert any(entry["status"] == "continue" for entry in results)
    assert "[OK]" in captured.out
    assert "[ERROR]" in captured.out
    assert "[CONTINUE]" in captured.out

    content = "".join(
        path.read_text(encoding="utf-8")
        for path in sorted(log_path.parent.glob("system.log*"))
    )
    assert "Simulation continues after controlled error." in content
    assert "Reservation processed successfully." in content
