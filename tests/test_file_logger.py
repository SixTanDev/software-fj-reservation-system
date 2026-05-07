"""Tests for the rotating file logger."""

from pathlib import Path

from software_fj_reservation_system.infrastructure.file_logger import FileLogger


def test_file_logger_creates_file_and_registers_event_and_error(tmp_path: Path) -> None:
    """The logger should create the target file and persist success and error entries."""

    log_path = tmp_path / "logs" / "system.log"
    logger = FileLogger(log_path=log_path)

    logger.log_event("register_client", "Client created successfully.", {"client_id": "1"})
    logger.log_error(
        "register_client",
        "Client creation failed.",
        ValueError("invalid client"),
        {"client_id": "2"},
    )
    logger.close()

    content = log_path.read_text(encoding="utf-8")
    assert "Client created successfully." in content
    assert "Client creation failed." in content
    assert "ValueError" in content


def test_file_logger_rotates_when_size_limit_is_reached(tmp_path: Path) -> None:
    """The rotating handler should create backup files when the size limit is exceeded."""

    log_path = tmp_path / "logs" / "system.log"
    logger = FileLogger(log_path=log_path, max_bytes=150, backup_count=2)

    for index in range(20):
        logger.log_event(
            "bulk_event",
            f"Event number {index} with enough content to rotate the file.",
            {"index": index},
        )

    logger.close()

    rotated_files = sorted(path.name for path in log_path.parent.glob("system.log*"))
    assert "system.log" in rotated_files
    assert any(name != "system.log" for name in rotated_files)


def test_file_logger_reuses_handler_pipeline_for_same_path(tmp_path: Path) -> None:
    """Multiple instances for the same path should not duplicate writes."""

    log_path = tmp_path / "logs" / "system.log"
    first_logger = FileLogger(log_path=log_path)
    second_logger = FileLogger(log_path=log_path)

    first_logger.log_event("first", "First logger entry.")
    second_logger.log_event("second", "Second logger entry.")

    first_logger.close()
    second_logger.close()

    content = log_path.read_text(encoding="utf-8")
    assert content.count("First logger entry.") == 1
    assert content.count("Second logger entry.") == 1
