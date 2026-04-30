from .service import Servicio

class AsesoriaEspecializada(Servicio):
    def __init__(self, id_servicio, nombre, precio_sesion, experto):
        super().__init__(id_servicio, nombre, precio_sesion)
        self.experto = experto

    # Sobrecarga con parámetros opcionales para impuestos o descuentos
    def calcular_costo(self, sesiones, impuesto=0.19, es_vip=False):
        subtotal = self._precio_base * sesiones
        if es_vip:
            subtotal *= 0.90  # 10% de descuento
        return subtotal + (subtotal * impuesto)

    def obtener_detalle(self):
        return f"Asesoría con: {self.experto} (Especialidad: {self.nombre})"