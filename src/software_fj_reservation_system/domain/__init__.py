"""Domain package exports.

This file makes it easier to import the domain classes from other layers.

For example, instead of importing each class from its individual file,
other modules can import them directly from the domain package.
"""

from software_fj_reservation_system.domain.client import Client
from software_fj_reservation_system.domain.consulting_service import ConsultingService
from software_fj_reservation_system.domain.entity import Entity
from software_fj_reservation_system.domain.equipment_service import EquipmentService
from software_fj_reservation_system.domain.reservation import Reservation
from software_fj_reservation_system.domain.room_service import RoomService
from software_fj_reservation_system.domain.service import Service

# __all__ defines which classes are publicly exported by this package.
__all__ = [
    "Client",
    "ConsultingService",
    "Entity",
    "EquipmentService",
    "Reservation",
    "RoomService",
    "Service",
]
