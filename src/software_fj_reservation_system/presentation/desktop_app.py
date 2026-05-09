"""Tkinter desktop application for the Software FJ reservation system."""

from __future__ import annotations

try:
    import tkinter as tk
    from tkinter import messagebox, ttk
except ImportError as error:
    tk = None  # type: ignore[assignment]
    ttk = None  # type: ignore[assignment]
    messagebox = None  # type: ignore[assignment]
    TKINTER_IMPORT_ERROR = error
else:
    TKINTER_IMPORT_ERROR = None

from software_fj_reservation_system.exceptions import (
    InconsistentCalculationError,
    InvalidDataError,
    InvalidReservationError,
    ManagementSystemError,
    OperationNotAllowedError,
    ServiceUnavailableError,
)
from software_fj_reservation_system.presentation.controller import (
    ReservationSystemController,
)
from software_fj_reservation_system.presentation.styles import PALETTE, configure_styles


def _ensure_tk_available() -> None:
    """Raise a clear error when Tk support is unavailable."""

    if TKINTER_IMPORT_ERROR is not None:
        raise RuntimeError(
            "Tkinter is not available in this Python environment."
        ) from TKINTER_IMPORT_ERROR


# pylint: disable=too-many-instance-attributes
class ReservationDesktopApp:
    """Tkinter/ttk desktop interface for the Software FJ system."""

    def __init__(
        self,
        root: tk.Tk | None = None,
        controller: ReservationSystemController | None = None,
    ) -> None:
        _ensure_tk_available()
        self.root = root or tk.Tk()
        self.controller = controller or ReservationSystemController()
        self._client_lookup: dict[str, str] = {}
        self._service_lookup: dict[str, str] = {}
        self._selected_reservation_id: str | None = None

        configure_styles(self.root)
        self.root.title("Software FJ Reservation System")
        self.root.geometry("1200x780")
        self.root.minsize(1100, 720)

        self.status_text = tk.StringVar(value=self.controller.last_operation_message)
        self.status_level = tk.StringVar(value=self.controller.last_operation_level)
        self.selected_reservation_text = tk.StringVar(
            value="Select a reservation from the table."
        )
        self.latest_event_text = tk.StringVar(value=self.controller.last_operation_message)
        self.client_count_text = tk.StringVar(value="0")
        self.service_count_text = tk.StringVar(value="0")
        self.reservation_count_text = tk.StringVar(value="0")
        self.last_status_text = tk.StringVar(value="Info")
        self.client_name_var = tk.StringVar()
        self.client_email_var = tk.StringVar()
        self.client_phone_var = tk.StringVar()
        self.service_type_var = tk.StringVar(value="room")
        self.service_name_var = tk.StringVar()
        self.service_base_price_var = tk.StringVar()
        self.service_extra_var = tk.StringVar()
        self.service_extra_label_var = tk.StringVar(value="Capacity")
        self.reservation_client_var = tk.StringVar()
        self.reservation_service_var = tk.StringVar()
        self.reservation_duration_var = tk.StringVar()
        self.process_tax_var = tk.StringVar(value="0")
        self.process_discount_var = tk.StringVar(value="0")
        self.dashboard_reservations_tree = None
        self.clients_tree = None
        self.services_tree = None
        self.client_combo = None
        self.service_combo = None
        self.reservations_tree = None
        self.logs_text = None

        self._build_layout()
        self._refresh_all_views()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def run(self) -> None:
        """Start the Tkinter event loop."""

        self.root.mainloop()

    def on_close(self) -> None:
        """Close logger resources before destroying the window."""

        self.controller.close()
        self.root.destroy()

    def _build_layout(self) -> None:
        """Build the application layout."""

        container = ttk.Frame(self.root, style="App.TFrame", padding=24)
        container.pack(fill="both", expand=True)
        container.columnconfigure(0, weight=1)
        container.rowconfigure(1, weight=1)

        header = ttk.Frame(container, style="Surface.TFrame", padding=24)
        header.grid(row=0, column=0, sticky="ew", pady=(0, 16))
        header.columnconfigure(0, weight=1)
        ttk.Label(
            header,
            text="Software FJ Reservation System",
            style="Title.TLabel",
        ).grid(row=0, column=0, sticky="w")
        ttk.Label(
            header,
            text="Clients, Services, Reservations and Robust Error Handling",
            style="Subtitle.TLabel",
        ).grid(row=1, column=0, sticky="w", pady=(6, 0))

        notebook = ttk.Notebook(container)
        notebook.grid(row=1, column=0, sticky="nsew")

        self.dashboard_tab = ttk.Frame(notebook, style="App.TFrame", padding=18)
        self.clients_tab = ttk.Frame(notebook, style="App.TFrame", padding=18)
        self.services_tab = ttk.Frame(notebook, style="App.TFrame", padding=18)
        self.reservations_tab = ttk.Frame(notebook, style="App.TFrame", padding=18)
        self.logs_tab = ttk.Frame(notebook, style="App.TFrame", padding=18)

        notebook.add(self.dashboard_tab, text="Dashboard")
        notebook.add(self.clients_tab, text="Clients")
        notebook.add(self.services_tab, text="Services")
        notebook.add(self.reservations_tab, text="Reservations")
        notebook.add(self.logs_tab, text="Logs")

        self._build_dashboard_tab()
        self._build_clients_tab()
        self._build_services_tab()
        self._build_reservations_tab()
        self._build_logs_tab()

        self.status_label = ttk.Label(
            container,
            textvariable=self.status_text,
            style="Status.TLabel",
        )
        self.status_label.grid(row=2, column=0, sticky="ew", pady=(16, 0))
        self._apply_status_style()

    def _build_dashboard_tab(self) -> None:
        """Build the dashboard tab."""

        for index in range(4):
            self.dashboard_tab.columnconfigure(index, weight=1, uniform="cards")
        self.dashboard_tab.rowconfigure(1, weight=1)

        self._build_summary_card(
            self.dashboard_tab,
            0,
            "Total Clients",
            self.client_count_text,
        )
        self._build_summary_card(
            self.dashboard_tab,
            1,
            "Total Services",
            self.service_count_text,
        )
        self._build_summary_card(
            self.dashboard_tab,
            2,
            "Total Reservations",
            self.reservation_count_text,
        )
        self._build_summary_card(
            self.dashboard_tab,
            3,
            "Last Status",
            self.last_status_text,
        )

        overview = ttk.LabelFrame(
            self.dashboard_tab,
            text="System Overview",
            style="Panel.TLabelframe",
            padding=16,
        )
        overview.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=(18, 0), padx=(0, 9))
        overview.columnconfigure(0, weight=1)
        ttk.Label(
            overview,
            text="Latest event",
            style="Section.TLabel",
        ).grid(row=0, column=0, sticky="w")
        ttk.Label(
            overview,
            textvariable=self.latest_event_text,
            style="Body.TLabel",
            wraplength=460,
            justify="left",
        ).grid(row=1, column=0, sticky="ew", pady=(8, 0))

        activity = ttk.LabelFrame(
            self.dashboard_tab,
            text="Recent Reservations",
            style="Panel.TLabelframe",
            padding=16,
        )
        activity.grid(row=1, column=2, columnspan=2, sticky="nsew", pady=(18, 0), padx=(9, 0))
        activity.columnconfigure(0, weight=1)
        activity.rowconfigure(0, weight=1)
        self.dashboard_reservations_tree = self._create_treeview(
            activity,
            columns=("id", "client", "service", "status"),
            headings={
                "id": "Reservation ID",
                "client": "Client",
                "service": "Service",
                "status": "Status",
            },
        )
        self.dashboard_reservations_tree.grid(row=0, column=0, sticky="nsew")

    def _build_summary_card(
        self,
        parent: ttk.Frame,
        column: int,
        title: str,
        value_var: tk.StringVar,
    ) -> None:
        """Build one summary card on the dashboard."""

        card = ttk.Frame(parent, style="Card.TFrame", padding=18)
        card.grid(row=0, column=column, sticky="nsew", padx=(0 if column == 0 else 6, 6))
        ttk.Label(card, text=title, style="Section.TLabel").pack(anchor="w")
        ttk.Label(card, textvariable=value_var, style="Metric.TLabel").pack(
            anchor="w",
            pady=(10, 0),
        )

    def _build_clients_tab(self) -> None:
        """Build the clients tab."""

        self.clients_tab.columnconfigure(1, weight=1)
        self.clients_tab.rowconfigure(0, weight=1)

        form = ttk.LabelFrame(
            self.clients_tab,
            text="Register Client",
            style="Panel.TLabelframe",
            padding=16,
        )
        form.grid(row=0, column=0, sticky="nsw", padx=(0, 12))

        self._add_labeled_entry(form, 0, "Name", self.client_name_var)
        self._add_labeled_entry(form, 1, "Email", self.client_email_var)
        self._add_labeled_entry(form, 2, "Phone", self.client_phone_var)
        ttk.Button(
            form,
            text="Register Client",
            style="Primary.TButton",
            command=self._register_client,
        ).grid(row=3, column=0, sticky="ew", pady=(16, 0))

        table_panel = ttk.LabelFrame(
            self.clients_tab,
            text="Registered Clients",
            style="Panel.TLabelframe",
            padding=16,
        )
        table_panel.grid(row=0, column=1, sticky="nsew")
        table_panel.columnconfigure(0, weight=1)
        table_panel.rowconfigure(0, weight=1)

        self.clients_tree = self._create_treeview(
            table_panel,
            columns=("id", "name", "email", "phone", "active"),
            headings={
                "id": "Client ID",
                "name": "Name",
                "email": "Email",
                "phone": "Phone",
                "active": "Active",
            },
        )
        self.clients_tree.grid(row=0, column=0, sticky="nsew")

    def _build_services_tab(self) -> None:
        """Build the services tab."""

        self.services_tab.columnconfigure(1, weight=1)
        self.services_tab.rowconfigure(0, weight=1)

        form = ttk.LabelFrame(
            self.services_tab,
            text="Create Service",
            style="Panel.TLabelframe",
            padding=16,
        )
        form.grid(row=0, column=0, sticky="nsw", padx=(0, 12))

        ttk.Label(form, text="Service Type", style="Muted.TLabel").grid(
            row=0,
            column=0,
            sticky="w",
        )
        service_type_combo = ttk.Combobox(
            form,
            textvariable=self.service_type_var,
            values=("room", "equipment", "consulting"),
            state="readonly",
        )
        service_type_combo.grid(row=1, column=0, sticky="ew", pady=(6, 12))
        service_type_combo.bind("<<ComboboxSelected>>", self._update_service_extra_field)

        self._add_labeled_entry(form, 2, "Name", self.service_name_var)
        self._add_labeled_entry(form, 4, "Base Price", self.service_base_price_var)
        ttk.Label(
            form,
            textvariable=self.service_extra_label_var,
            style="Muted.TLabel",
        ).grid(row=6, column=0, sticky="w")
        ttk.Entry(form, textvariable=self.service_extra_var).grid(
            row=7,
            column=0,
            sticky="ew",
            pady=(6, 12),
        )
        ttk.Button(
            form,
            text="Create Service",
            style="Primary.TButton",
            command=self._create_service,
        ).grid(row=8, column=0, sticky="ew", pady=(16, 0))

        table_panel = ttk.LabelFrame(
            self.services_tab,
            text="Available Services",
            style="Panel.TLabelframe",
            padding=16,
        )
        table_panel.grid(row=0, column=1, sticky="nsew")
        table_panel.columnconfigure(0, weight=1)
        table_panel.rowconfigure(0, weight=1)

        self.services_tree = self._create_treeview(
            table_panel,
            columns=("id", "type", "name", "price", "availability", "details"),
            headings={
                "id": "Service ID",
                "type": "Type",
                "name": "Name",
                "price": "Base Price",
                "availability": "Available",
                "details": "Details",
            },
        )
        self.services_tree.grid(row=0, column=0, sticky="nsew")

    def _build_reservations_tab(self) -> None:
        """Build the reservations tab."""

        for index in range(2):
            self.reservations_tab.columnconfigure(index, weight=1)
        self.reservations_tab.rowconfigure(1, weight=1)

        create_panel = ttk.LabelFrame(
            self.reservations_tab,
            text="Create Reservation",
            style="Panel.TLabelframe",
            padding=16,
        )
        create_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 12))

        ttk.Label(create_panel, text="Client", style="Muted.TLabel").grid(
            row=0,
            column=0,
            sticky="w",
        )
        self.client_combo = ttk.Combobox(
            create_panel,
            textvariable=self.reservation_client_var,
            state="readonly",
        )
        self.client_combo.grid(row=1, column=0, sticky="ew", pady=(6, 12))

        ttk.Label(create_panel, text="Service", style="Muted.TLabel").grid(
            row=2,
            column=0,
            sticky="w",
        )
        self.service_combo = ttk.Combobox(
            create_panel,
            textvariable=self.reservation_service_var,
            state="readonly",
        )
        self.service_combo.grid(row=3, column=0, sticky="ew", pady=(6, 12))

        self._add_labeled_entry(
            create_panel,
            4,
            "Duration",
            self.reservation_duration_var,
        )
        ttk.Button(
            create_panel,
            text="Create Reservation",
            style="Primary.TButton",
            command=self._create_reservation,
        ).grid(row=6, column=0, sticky="ew", pady=(16, 0))

        manage_panel = ttk.LabelFrame(
            self.reservations_tab,
            text="Manage Reservation",
            style="Panel.TLabelframe",
            padding=16,
        )
        manage_panel.grid(row=0, column=1, sticky="nsew")
        manage_panel.columnconfigure(0, weight=1)
        ttk.Label(
            manage_panel,
            textvariable=self.selected_reservation_text,
            style="Body.TLabel",
            wraplength=440,
            justify="left",
        ).grid(row=0, column=0, sticky="ew", pady=(0, 12))

        button_row = ttk.Frame(manage_panel, style="Surface.TFrame")
        button_row.grid(row=1, column=0, sticky="ew")
        for index in range(3):
            button_row.columnconfigure(index, weight=1, uniform="actions")
        ttk.Button(
            button_row,
            text="Confirm",
            style="Primary.TButton",
            command=self._confirm_reservation,
        ).grid(row=0, column=0, sticky="ew", padx=(0, 6))
        ttk.Button(
            button_row,
            text="Cancel",
            style="Secondary.TButton",
            command=self._cancel_reservation,
        ).grid(row=0, column=1, sticky="ew", padx=6)
        ttk.Button(
            button_row,
            text="Process",
            style="Primary.TButton",
            command=self._process_reservation,
        ).grid(row=0, column=2, sticky="ew", padx=(6, 0))

        self._add_labeled_entry(manage_panel, 2, "Tax Rate", self.process_tax_var)
        self._add_labeled_entry(
            manage_panel,
            4,
            "Discount Rate",
            self.process_discount_var,
        )

        table_panel = ttk.LabelFrame(
            self.reservations_tab,
            text="Reservations",
            style="Panel.TLabelframe",
            padding=16,
        )
        table_panel.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=(18, 0))
        table_panel.columnconfigure(0, weight=1)
        table_panel.rowconfigure(0, weight=1)

        self.reservations_tree = self._create_treeview(
            table_panel,
            columns=("id", "client", "service", "duration", "status"),
            headings={
                "id": "Reservation ID",
                "client": "Client",
                "service": "Service",
                "duration": "Duration",
                "status": "Status",
            },
        )
        self.reservations_tree.grid(row=0, column=0, sticky="nsew")
        self.reservations_tree.bind("<<TreeviewSelect>>", self._on_reservation_selected)

    def _build_logs_tab(self) -> None:
        """Build the logs tab."""

        self.logs_tab.columnconfigure(0, weight=1)
        self.logs_tab.rowconfigure(1, weight=1)

        controls = ttk.Frame(self.logs_tab, style="App.TFrame")
        controls.grid(row=0, column=0, sticky="ew", pady=(0, 12))
        controls.columnconfigure(1, weight=1)
        ttk.Button(
            controls,
            text="Refresh Logs",
            style="Primary.TButton",
            command=self._load_logs,
        ).grid(row=0, column=0, sticky="w")
        ttk.Label(
            controls,
            text=f"Source: {self.controller.logger.log_path}",
            style="Muted.TLabel",
        ).grid(row=0, column=1, sticky="e")

        log_panel = ttk.LabelFrame(
            self.logs_tab,
            text="System Log",
            style="Panel.TLabelframe",
            padding=16,
        )
        log_panel.grid(row=1, column=0, sticky="nsew")
        log_panel.columnconfigure(0, weight=1)
        log_panel.rowconfigure(0, weight=1)

        self.logs_text = tk.Text(
            log_panel,
            bg=PALETTE["surface"],
            fg=PALETTE["text"],
            insertbackground=PALETTE["text"],
            relief="flat",
            wrap="none",
            font=("Menlo", 10),
            padx=10,
            pady=10,
        )
        self.logs_text.grid(row=0, column=0, sticky="nsew")
        self.logs_text.configure(state="disabled")
        scrollbar = ttk.Scrollbar(log_panel, command=self.logs_text.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.logs_text.configure(yscrollcommand=scrollbar.set)

    def _add_labeled_entry(
        self,
        parent: ttk.LabelFrame,
        row: int,
        label: str,
        variable: tk.StringVar,
    ) -> None:
        """Add a standard label/entry pair to a form."""

        ttk.Label(parent, text=label, style="Muted.TLabel").grid(
            row=row,
            column=0,
            sticky="w",
        )
        ttk.Entry(parent, textvariable=variable).grid(
            row=row + 1,
            column=0,
            sticky="ew",
            pady=(6, 12),
        )

    def _create_treeview(
        self,
        parent: ttk.Widget,
        columns: tuple[str, ...],
        headings: dict[str, str],
    ) -> ttk.Treeview:
        """Create a configured treeview with shared defaults."""

        tree = ttk.Treeview(parent, columns=columns, show="headings")
        for column in columns:
            tree.heading(column, text=headings[column])
            tree.column(column, anchor="w", stretch=True, width=150)
        return tree

    def _register_client(self) -> None:
        """Handle the register client action."""

        try:
            self.controller.register_client(
                self.client_name_var.get(),
                self.client_email_var.get(),
                self.client_phone_var.get(),
            )
        except self._controlled_exceptions():
            self._sync_status()
            return
        except Exception as error:  # pylint: disable=broad-exception-caught
            self._handle_unexpected_error("register_client", error)
            return

        self.client_name_var.set("")
        self.client_email_var.set("")
        self.client_phone_var.set("")
        self._refresh_all_views()

    def _create_service(self) -> None:
        """Handle the create service action."""

        try:
            self.controller.create_service(
                self.service_type_var.get(),
                self.service_name_var.get(),
                self.service_base_price_var.get(),
                self.service_extra_var.get(),
            )
        except self._controlled_exceptions():
            self._sync_status()
            return
        except Exception as error:  # pylint: disable=broad-exception-caught
            self._handle_unexpected_error("create_service", error)
            return

        self.service_name_var.set("")
        self.service_base_price_var.set("")
        self.service_extra_var.set("")
        self._refresh_all_views()

    def _create_reservation(self) -> None:
        """Handle the create reservation action."""

        client_id = self._client_lookup.get(self.reservation_client_var.get(), "")
        service_id = self._service_lookup.get(self.reservation_service_var.get(), "")

        try:
            self.controller.create_reservation(
                client_id,
                service_id,
                self.reservation_duration_var.get(),
            )
        except self._controlled_exceptions():
            self._sync_status()
            return
        except Exception as error:  # pylint: disable=broad-exception-caught
            self._handle_unexpected_error("create_reservation", error)
            return

        self.reservation_duration_var.set("")
        self._refresh_all_views()

    def _confirm_reservation(self) -> None:
        """Handle reservation confirmation."""

        if not self._selected_reservation_id:
            self._set_ui_status("warning", "Select a reservation before confirming it.")
            return

        try:
            self.controller.confirm_reservation(self._selected_reservation_id)
        except self._controlled_exceptions():
            self._sync_status()
            return
        except Exception as error:  # pylint: disable=broad-exception-caught
            self._handle_unexpected_error("confirm_reservation", error)
            return

        self._refresh_all_views()

    def _cancel_reservation(self) -> None:
        """Handle reservation cancellation."""

        if not self._selected_reservation_id:
            self._set_ui_status("warning", "Select a reservation before cancelling it.")
            return

        try:
            self.controller.cancel_reservation(self._selected_reservation_id)
        except self._controlled_exceptions():
            self._sync_status()
            return
        except Exception as error:  # pylint: disable=broad-exception-caught
            self._handle_unexpected_error("cancel_reservation", error)
            return

        self._refresh_all_views()

    def _process_reservation(self) -> None:
        """Handle reservation processing."""

        if not self._selected_reservation_id:
            self._set_ui_status("warning", "Select a reservation before processing it.")
            return

        try:
            self.controller.process_reservation(
                self._selected_reservation_id,
                self.process_tax_var.get(),
                self.process_discount_var.get(),
            )
        except self._controlled_exceptions():
            self._sync_status()
            return
        except Exception as error:  # pylint: disable=broad-exception-caught
            self._handle_unexpected_error("process_reservation", error)
            return

        self._refresh_all_views()

    def _load_logs(self) -> None:
        """Load the latest log entries into the readonly text view."""

        try:
            content = self.controller.read_logs(update_status=True)
        except OSError as error:
            self._handle_unexpected_error("load_logs", error)
            return

        self._set_logs_text(content)
        self._sync_status()

    def _set_logs_text(self, content: str) -> None:
        """Replace the readonly log text content."""

        self.logs_text.configure(state="normal")
        self.logs_text.delete("1.0", "end")
        self.logs_text.insert("1.0", content)
        self.logs_text.configure(state="disabled")

    def _refresh_all_views(self) -> None:
        """Refresh dashboard, tables, selectors, and status labels."""

        self._refresh_dashboard()
        self._refresh_clients_table()
        self._refresh_services_table()
        self._refresh_reservations_table()
        self._refresh_reservation_selectors()
        self._set_logs_text(self.controller.read_logs(update_status=False))
        self._sync_status()

    def _refresh_dashboard(self) -> None:
        """Refresh the dashboard counters and recent reservation view."""

        counts = self.controller.dashboard_counts()
        self.client_count_text.set(str(counts["clients"]))
        self.service_count_text.set(str(counts["services"]))
        self.reservation_count_text.set(str(counts["reservations"]))
        self.last_status_text.set(self.controller.last_operation_level.title())
        self.latest_event_text.set(self.controller.last_operation_message)

        self._replace_tree_items(
            self.dashboard_reservations_tree,
            [
                (
                    reservation.id,
                    reservation.client.name,
                    reservation.service.name,
                    reservation.status.title(),
                )
                for reservation in self.controller.list_reservations()[-8:]
            ],
        )

    def _refresh_clients_table(self) -> None:
        """Refresh the client table."""

        self._replace_tree_items(
            self.clients_tree,
            [
                (
                    client.id,
                    client.name,
                    client.email,
                    client.phone,
                    "Yes" if client.active else "No",
                )
                for client in self.controller.list_clients()
            ],
        )

    def _refresh_services_table(self) -> None:
        """Refresh the service table."""

        service_rows = []
        for service in self.controller.list_services():
            service_rows.append(
                (
                    service.id,
                    type(service).__name__.replace("Service", ""),
                    service.name,
                    f"{service.base_price:,.2f}",
                    "Yes" if service.available else "No",
                    service.describe(),
                )
            )
        self._replace_tree_items(self.services_tree, service_rows)

    def _refresh_reservations_table(self) -> None:
        """Refresh the reservation table."""

        rows = [
            (
                reservation.id,
                reservation.client.name,
                reservation.service.name,
                str(reservation.duration),
                reservation.status.title(),
            )
            for reservation in self.controller.list_reservations()
        ]
        self._replace_tree_items(self.reservations_tree, rows)
        self._restore_selected_reservation()

    def _refresh_reservation_selectors(self) -> None:
        """Refresh the client and service selectors used by the reservation form."""

        self._client_lookup = {
            f"{client.name} [{client.id}]": client.id
            for client in self.controller.list_clients()
        }
        self._service_lookup = {
            f"{service.name} [{service.id}]": service.id
            for service in self.controller.list_services()
        }
        self.client_combo.configure(values=tuple(self._client_lookup))
        self.service_combo.configure(values=tuple(self._service_lookup))

        if self.reservation_client_var.get() not in self._client_lookup:
            self.reservation_client_var.set("")
        if self.reservation_service_var.get() not in self._service_lookup:
            self.reservation_service_var.set("")

    def _replace_tree_items(
        self,
        tree: ttk.Treeview,
        rows: list[tuple[str, ...]],
    ) -> None:
        """Replace all rows in a treeview."""

        for item in tree.get_children():
            tree.delete(item)
        for row in rows:
            tree.insert("", "end", values=row)

    def _on_reservation_selected(self, _event: tk.Event[tk.Misc]) -> None:
        """Capture the selected reservation from the treeview."""

        selection = self.reservations_tree.selection()
        if not selection:
            self._selected_reservation_id = None
            self.selected_reservation_text.set("Select a reservation from the table.")
            return

        values = self.reservations_tree.item(selection[0], "values")
        self._selected_reservation_id = str(values[0])
        self.selected_reservation_text.set(
            (
                f"Selected reservation: {values[0]} | Client: {values[1]} | "
                f"Service: {values[2]} | Status: {values[4]}"
            )
        )

    def _restore_selected_reservation(self) -> None:
        """Restore the current reservation selection after refreshing the table."""

        if not self._selected_reservation_id:
            return

        for item in self.reservations_tree.get_children():
            values = self.reservations_tree.item(item, "values")
            if values and values[0] == self._selected_reservation_id:
                self.reservations_tree.selection_set(item)
                self.reservations_tree.focus(item)
                self.selected_reservation_text.set(
                    (
                        f"Selected reservation: {values[0]} | Client: {values[1]} | "
                        f"Service: {values[2]} | Status: {values[4]}"
                    )
                )
                return

        self._selected_reservation_id = None
        self.selected_reservation_text.set("Select a reservation from the table.")

    def _update_service_extra_field(self, _event: tk.Event[tk.Misc] | None = None) -> None:
        """Update the extra service field label based on the selected type."""

        label_by_type = {
            "room": "Capacity",
            "equipment": "Equipment Type",
            "consulting": "Consultant Name",
        }
        self.service_extra_label_var.set(label_by_type.get(self.service_type_var.get(), "Details"))

    def _sync_status(self) -> None:
        """Synchronize the status bar with the controller status."""

        self.status_text.set(self.controller.last_operation_message)
        self.status_level.set(self.controller.last_operation_level)
        self.latest_event_text.set(self.controller.last_operation_message)
        self.last_status_text.set(self.controller.last_operation_level.title())
        self._apply_status_style()

    def _apply_status_style(self) -> None:
        """Apply the status color to the status bar."""

        color = {
            "success": PALETTE["success"],
            "error": PALETTE["error"],
            "warning": PALETTE["warning"],
            "info": PALETTE["text"],
        }.get(self.status_level.get(), PALETTE["text"])
        self.status_label.configure(foreground=color)

    def _set_ui_status(self, level: str, message: str) -> None:
        """Set a UI-only status message."""

        self.controller.last_operation_level = level
        self.controller.last_operation_message = message
        self._sync_status()

    def _handle_unexpected_error(self, operation: str, error: Exception) -> None:
        """Log and surface unexpected UI errors."""

        self.controller.logger.log_error(
            operation,
            "Unexpected desktop UI error.",
            error,
            state={"selected_reservation_id": self._selected_reservation_id or ""},
        )
        self._set_ui_status("error", "An unexpected desktop UI error occurred.")
        messagebox.showerror("Software FJ", f"Unexpected error: {error}")

    @staticmethod
    def _controlled_exceptions() -> tuple[type[Exception], ...]:
        """Return the controlled exceptions surfaced by the application."""

        return (
            InvalidDataError,
            InvalidReservationError,
            ServiceUnavailableError,
            OperationNotAllowedError,
            InconsistentCalculationError,
            ManagementSystemError,
        )


def main() -> None:
    """Run the desktop application."""

    if TKINTER_IMPORT_ERROR is not None:
        raise SystemExit(
            "Tkinter UI could not start because this Python environment does not "
            f"include Tk support: {TKINTER_IMPORT_ERROR}"
        ) from TKINTER_IMPORT_ERROR

    try:
        app = ReservationDesktopApp()
    except tk.TclError as error:
        raise SystemExit(
            f"Tkinter UI could not start because no display is available: {error}"
        ) from error

    app.run()


if __name__ == "__main__":
    main()
