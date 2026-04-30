from .service import Servicio

class ReservaSala(Servicio):
    def __init__(self, id_servicio, nombre, precio_base, capacidad):
        super().__init__(id_servicio, nombre, precio_base)
        self.capacidad = capacidad

    def calcular_costo(self, horas):
        # Polimorfismo: cálculo basado en horas
        return self._precio_base * horas

    def obtener_detalle(self):
        return f"Sala: {self.nombre} (Capacidad: {self.capacidad} personas)"