from abc import ABC, abstractmethod
from datetime import datetime

class EntidadBase(ABC):
    def __init__(self, id_entidad):
        self._id_entidad = id_entidad
        self._fecha_creacion = datetime.now()

    @property
    def id_entidad(self):
        return self._id_entidad