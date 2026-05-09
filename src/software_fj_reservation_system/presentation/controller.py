"""Controller layer for the Tkinter desktop application."""

from __future__ import annotations

from dataclasses import dataclass, field

from software_fj_reservation_system.application.create_reservation import (
    create_reservation,
)
from software_fj_reservation_system.application.create_service import create_service
from software_fj_reservation_system.application.manage_reservation import (
    cancel_reservation,
    confirm_reservation,
    process_reservation,
)
from software_fj_reservation_system.application.register_client import register_client
from software_fj_reservation_system.domain.client import Client
from software_fj_reservation_system.domain.reservation import Reservation
from software_fj_reservation_system.domain.service import Service
from software_fj_reservation_system.exceptions import ManagementSystemError
from software_fj_reservation_system.infrastructure.client_repository import (
    ClientRepositoryInMemory,
)
from software_fj_reservation_system.infrastructure.file_logger import FileLogger
from software_fj_reservation_system.infrastructure.reservation_repository import (
    ReservationRepositoryInMemory,
)
from software_fj_reservation_system.infrastructure.service_repository import (
    ServiceRepositoryInMemory,
)


@dataclass
class ReservationSystemController:
    """Stateful controller that delegates operations to the existing use cases."""

    client_repository: ClientRepositoryInMemory = field(
        default_factory=ClientRepositoryInMemory
    )
    service_repository: ServiceRepositoryInMemory = field(
        default_factory=ServiceRepositoryInMemory
    )
    reservation_repository: ReservationRepositoryInMemory = field(
        default_factory=ReservationRepositoryInMemory
    )
    logger: FileLogger = field(default_factory=FileLogger)
    last_operation_message: str = "System ready."
    last_operation_level: str = "info"

    def register_client(self, name: str, email: str, phone: str) -> Client:
        """Register a client through the application layer."""

        try:
            client = register_client(
                self.client_repository,
                self.logger,
                {"name": name, "email": email, "phone": phone},
            )
        except ManagementSystemError as error:
            self._set_status("error", str(error))
            raise

        self._set_status("success", f"Client '{client.name}' registered successfully.")
        return client

    def create_service(
        self,
        service_type: str,
        name: str,
        base_price: str,
        extra_value: str,
    ) -> Service:
        """Create a service through the application layer."""

        payload: dict[str, object] = {
            "service_type": service_type,
            "name": name,
            "base_price": base_price,
        }
        if service_type == "room":
            payload["capacity"] = extra_value
        elif service_type == "equipment":
            payload["equipment_type"] = extra_value
        elif service_type == "consulting":
            payload["consultant_name"] = extra_value

        try:
            service = create_service(self.service_repository, self.logger, payload)
        except ManagementSystemError as error:
            self._set_status("error", str(error))
            raise

        self._set_status(
            "success",
            f"Service '{service.name}' created successfully.",
        )
        return service

    def create_reservation(
        self,
        client_id: str,
        service_id: str,
        duration: str,
    ) -> Reservation:
        """Create a reservation through the application layer."""

        try:
            reservation = create_reservation(
                self.reservation_repository,
                self.client_repository,
                self.service_repository,
                self.logger,
                {
                    "client_id": client_id,
                    "service_id": service_id,
                    "duration": duration,
                },
            )
        except ManagementSystemError as error:
            self._set_status("error", str(error))
            raise

        self._set_status(
            "success",
            f"Reservation '{reservation.id}' created successfully.",
        )
        return reservation

    def confirm_reservation(self, reservation_id: str) -> Reservation:
        """Confirm the selected reservation."""

        try:
            reservation = confirm_reservation(
                self.reservation_repository,
                self.logger,
                reservation_id,
            )
        except ManagementSystemError as error:
            self._set_status("error", str(error))
            raise

        self._set_status(
            "success",
            f"Reservation '{reservation.id}' confirmed successfully.",
        )
        return reservation

    def cancel_reservation(self, reservation_id: str) -> Reservation:
        """Cancel the selected reservation."""

        try:
            reservation = cancel_reservation(
                self.reservation_repository,
                self.logger,
                reservation_id,
            )
        except ManagementSystemError as error:
            self._set_status("error", str(error))
            raise

        self._set_status(
            "success",
            f"Reservation '{reservation.id}' cancelled successfully.",
        )
        return reservation

    def process_reservation(
        self,
        reservation_id: str,
        tax_rate: str,
        discount_rate: str,
    ) -> float:
        """Process the selected reservation and return the total cost."""

        try:
            total_cost = process_reservation(
                self.reservation_repository,
                self.logger,
                {
                    "reservation_id": reservation_id,
                    "tax_rate": tax_rate or 0,
                    "discount_rate": discount_rate or 0,
                },
            )
        except ManagementSystemError as error:
            self._set_status("error", str(error))
            raise

        self._set_status(
            "success",
            (
                f"Reservation '{reservation_id}' processed successfully. "
                f"Total: {total_cost:,.2f}"
            ),
        )
        return total_cost

    def list_clients(self) -> list[Client]:
        """Return the registered clients."""

        return self.client_repository.list_all()

    def list_services(self) -> list[Service]:
        """Return the registered services."""

        return self.service_repository.list_all()

    def list_reservations(self) -> list[Reservation]:
        """Return the registered reservations."""

        return self.reservation_repository.list_all()

    def read_logs(self, max_lines: int = 120, update_status: bool = True) -> str:
        """Read the latest log lines from the configured log file."""

        if not self.logger.log_path.exists():
            if update_status:
                self._set_status("warning", "No log file is available yet.")
            return "No log entries available yet."

        try:
            lines = self.logger.log_path.read_text(encoding="utf-8").splitlines()
        except OSError as error:
            self.logger.log_error(
                "load_logs",
                "Failed to read the log file.",
                error,
                state={"log_path": str(self.logger.log_path)},
            )
            raise

        if update_status:
            self._set_status("info", "Loaded the latest log entries.")
        return "\n".join(lines[-max_lines:]) or "No log entries available yet."

    def close(self) -> None:
        """Close the shared logger resources."""

        self.logger.close()

    def dashboard_counts(self) -> dict[str, int]:
        """Return the dashboard counters for the main entities."""

        return {
            "clients": len(self.list_clients()),
            "services": len(self.list_services()),
            "reservations": len(self.list_reservations()),
        }

    def _set_status(self, level: str, message: str) -> None:
        """Store the latest controller status for the dashboard and status bar."""

        self.last_operation_level = level
        self.last_operation_message = message
