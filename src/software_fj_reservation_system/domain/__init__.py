"""
Domain package.
This package contains the main business entities of the system:
Client, Service, and Reservation.
"""

# Esto es lo que debes agregar debajo de las comillas:
from .entity import EntidadBase
from .service import Servicio
from .client import Cliente
from .room_service import ReservaSala
from .equipment_service import AlquilerEquipo
from .consulting_service import AsesoriaEspecializada
from .reservation import Reserva
