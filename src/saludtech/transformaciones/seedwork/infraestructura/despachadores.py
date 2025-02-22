import pulsar
from pulsar.schema import AvroSchema
from abc import ABC, abstractmethod
from saludtech.transformaciones.seedwork.infraestructura import utils
from functools import singledispatch

class DespachadorBase(ABC):
    @abstractmethod
    def publicar_evento(self, evento, topico):
        pass

    @abstractmethod
    def publicar_comando(self, comando, topico):
        pass

@singledispatch
def publicar_mensaje(comando):
    raise NotImplementedError(f'No existe implementación para el comando de tipo {type(comando).__name__}')