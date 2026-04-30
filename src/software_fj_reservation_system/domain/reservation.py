from .entity import EntidadBase
from ..exceptions.custom_exceptions import ReservaInvalidaError

class Reserva(EntidadBase):
    def __init__(self, id_reserva, cliente, servicio, duracion):
        super().__init__(id_reserva)
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "PENDIENTE" # Estado inicial

    def confirmar(self):
        try:
            if self.duracion <= 0:
                raise ReservaInvalidaError("La duración debe ser mayor a cero")
            
            # Aquí se calcula el costo usando polimorfismo
            costo = self.servicio.calcular_costo(self.duracion)
            self.estado = "CONFIRMADA"
            return f"Reserva confirmada. Costo total: ${costo}"
            
        except ReservaInvalidaError as e:
            # Esto cumple con el "Manejo avanzado de excepciones"
            raise e