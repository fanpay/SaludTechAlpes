""" Fábricas para la creación de objetos en la capa de infrastructura del dominio de anonimizacion

En este archivo usted encontrará las diferentes fábricas para crear
objetos complejos en la capa de infraestructura del dominio de anonimizacion

"""

from dataclasses import dataclass
from saludtech.procesamiento.seedwork.dominio.fabricas import Fabrica
from saludtech.procesamiento.seedwork.dominio.repositorios import Repositorio
from saludtech.procesamiento.modulos.procesamiento.dominio.repositorios import RepositorioImagenes, RepositorioProcesosAnonimizacion
from .repositorios import RepositorioImagenesDB, RepositorioProcesosAnonimizacionDB
from .excepciones import ExcepcionFabrica

@dataclass
class FabricaRepositorio(Fabrica):
    def crear_objeto(self, obj: type, mapeador: any = None) -> Repositorio:
        return RepositorioImagenesDB()