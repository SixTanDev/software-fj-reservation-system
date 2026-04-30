from abc import abstractmethod
from .entity import EntidadBase

class Servicio(EntidadBase):
    def __init__(self, id_servicio, nombre, precio_base):
        super().__init__(id_servicio)
        self.nombre = nombre
        self._precio_base = precio_base # Encapsulación

    @abstractmethod
    def calcular_costo(self, **kwargs):
        """Este método es polimórfico: cada servicio lo implementa distinto"""
        pass

    @abstractmethod
    def obtener_detalle(self):
        """Devuelve una descripción del servicio"""
        pass