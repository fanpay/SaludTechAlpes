""" Fábricas para la creación de objetos en la capa de infrastructura del dominio de anonimizacion

En este archivo usted encontrará las diferentes fábricas para crear
objetos complejos en la capa de infraestructura del dominio de anonimizacion

"""

from dataclasses import dataclass, field
from saludtech.transformaciones.seedwork.dominio.fabricas import Fabrica
from saludtech.transformaciones.seedwork.dominio.repositorios import Repositorio
from saludtech.transformaciones.modulos.anonimizacion.dominio.repositorios import RepositorioImagenesAnonimizadas, RepositorioProcesosAnonimizacion
from .repositorios import RepositorioReservasSQLite, RepositorioProveedoresSQLite
from .excepciones import ExcepcionFabrica

@dataclass
class FabricaRepositorio(Fabrica):
    def crear_objeto(self, obj: type, mapeador: any = None) -> Repositorio:
        if obj == RepositorioImagenesAnonimizadas.__class__:
            return RepositorioReservasSQLite()
        elif obj == RepositorioProcesosAnonimizacion.__class__:
            return RepositorioProveedoresSQLite()
        else:
            raise ExcepcionFabrica()