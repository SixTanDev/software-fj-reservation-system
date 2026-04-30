from .service import Servicio

class AlquilerEquipo(Servicio):
    def __init__(self, id_servicio, nombre, precio_dia, marca):
        super().__init__(id_servicio, nombre, precio_dia)
        self.marca = marca

    # Simulamos sobrecarga con el parámetro opcional 'seguro'
    def calcular_costo(self, dias, seguro=0):
        total = self._precio_base * dias
        if seguro > 0:
            total += seguro
        return total

    def obtener_detalle(self):
        return f"Equipo: {self.nombre} (Marca: {self.marca})"