"""Centralized file logger for the Software FJ reservation system.

The logger uses a queue and a single listener so application code can enqueue
messages safely while only one writer thread touches the rotating log file.
This reduces the risk of concurrent writes and keeps the implementation within
the Python standard library.
"""

from __future__ import annotations

from dataclasses import dataclass
import logging
from logging.handlers import QueueHandler, QueueListener, RotatingFileHandler
from pathlib import Path
from queue import Queue
import threading
from typing import Any

from software_fj_reservation_system.exceptions import LoggingError


@dataclass
class _LoggerResources:
    """Shared logger resources for one physical log path."""

    logger: logging.Logger
    queue_handler: QueueHandler
    listener: QueueListener
    file_handler: RotatingFileHandler
    references: int = 0


class FileLogger:
    """Safe file logger with rotation and queue-based serialization."""

    _resources_by_path: dict[Path, _LoggerResources] = {}
    _registry_lock = threading.Lock()

    def __init__(
        self,
        log_path: str | Path = "logs/system.log",
        max_bytes: int = 1_048_576,
        backup_count: int = 3,
        raise_logging_errors: bool = False,
    ) -> None:
        self._log_path = Path(log_path).expanduser().resolve()
        self._max_bytes = max_bytes
        self._backup_count = backup_count
        self._raise_logging_errors = raise_logging_errors
        self._closed = False
        self._resources = self._acquire_resources()
        self._logger = self._resources.logger

    @property
    def log_path(self) -> Path:
        """Return the physical path used by the rotating file handler."""

        return self._log_path

    def log_event(
        self,
        operation: str,
        message: str,
        state: dict[str, Any] | None = None,
    ) -> None:
        """Record an informational event without breaking the main flow."""

        self._log(
            level=logging.INFO,
            message=message,
            extra=self._build_extra(operation=operation, error=None, state=state),
        )

    def log_warning(
        self,
        operation: str,
        message: str,
        state: dict[str, Any] | None = None,
    ) -> None:
        """Record a warning without breaking the main flow."""

        self._log(
            level=logging.WARNING,
            message=message,
            extra=self._build_extra(operation=operation, error=None, state=state),
        )

    def log_error(
        self,
        operation: str,
        message: str,
        error: Exception,
        state: dict[str, Any] | None = None,
    ) -> None:
        """Record a controlled failure without breaking the main flow."""

        self._log(
            level=logging.ERROR,
            message=message,
            extra=self._build_extra(operation=operation, error=error, state=state),
        )

    def close(self) -> None:
        """Release the shared listener when this instance is no longer needed."""

        if self._closed:
            return

        with self._registry_lock:
            resources = self._resources_by_path.get(self._log_path)
            if resources is None:
                self._closed = True
                return

            resources.references -= 1
            if resources.references == 0:
                resources.logger.removeHandler(resources.queue_handler)
                resources.listener.stop()
                resources.file_handler.close()
                self._resources_by_path.pop(self._log_path, None)

        self._closed = True

    shutdown = close

    def _acquire_resources(self) -> _LoggerResources:
        """Create or reuse the logger pipeline for the configured path."""

        with self._registry_lock:
            resources = self._resources_by_path.get(self._log_path)
            if resources is None:
                self._log_path.parent.mkdir(parents=True, exist_ok=True)
                queue_handler, listener, file_handler = self._build_pipeline()
                logger = logging.getLogger(
                    "software_fj_reservation_system."
                    f"{abs(hash(self._log_path.as_posix()))}"
                )
                logger.setLevel(logging.INFO)
                logger.propagate = False
                logger.handlers = [
                    handler
                    for handler in logger.handlers
                    if not isinstance(handler, QueueHandler)
                ]
                logger.addHandler(queue_handler)
                resources = _LoggerResources(
                    logger=logger,
                    queue_handler=queue_handler,
                    listener=listener,
                    file_handler=file_handler,
                    references=0,
                )
                listener.start()
                self._resources_by_path[self._log_path] = resources

            resources.references += 1
            return resources

    def _build_pipeline(
        self,
    ) -> tuple[QueueHandler, QueueListener, RotatingFileHandler]:
        """Create the queue handler, rotating file handler, and listener."""

        log_queue: Queue[logging.LogRecord] = Queue()
        queue_handler = QueueHandler(log_queue)
        file_handler = RotatingFileHandler(
            self._log_path,
            maxBytes=self._max_bytes,
            backupCount=self._backup_count,
            encoding="utf-8",
            delay=True,
        )
        formatter = logging.Formatter(
            fmt=(
                "%(asctime)s | %(levelname)s | %(operation)s | %(message)s "
                "| error=%(error_type)s | state=%(state)s"
            ),
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.INFO)
        listener = QueueListener(log_queue, file_handler, respect_handler_level=True)
        return queue_handler, listener, file_handler

    def _log(
        self,
        level: int,
        message: str,
        extra: dict[str, Any],
    ) -> None:
        """Enqueue a log record and optionally surface controlled logger failures."""

        if self._closed:
            return

        try:
            self._logger.log(level, message, extra=extra)
        except Exception as log_error:  # pylint: disable=broad-exception-caught
            if self._raise_logging_errors:
                raise LoggingError("Failed to persist log entry.") from log_error

    @staticmethod
    def _build_extra(
        operation: str,
        error: Exception | None,
        state: dict[str, Any] | None,
    ) -> dict[str, Any]:
        """Build the structured fields expected by the log formatter."""

        return {
            "operation": operation,
            "error_type": type(error).__name__ if error is not None else "-",
            "state": state or {},
        }
