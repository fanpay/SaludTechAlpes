""" Fábricas para la creación de objetos en la capa de infrastructura del dominio de anonimizacion

En este archivo usted encontrará las diferentes fábricas para crear
objetos complejos en la capa de infraestructura del dominio de anonimizacion

"""

from dataclasses import dataclass
from saludtech.transformaciones.seedwork.dominio.fabricas import Fabrica
from saludtech.transformaciones.seedwork.dominio.repositorios import Repositorio
from saludtech.transformaciones.modulos.anonimizacion.dominio.repositorios import RepositorioImagenesAnonimizadas, RepositorioProcesosAnonimizacion
from .repositorios import RepositorioImagenesAnonimizadasSQLite, RepositorioProcesosAnonimizacionSQLite
from .excepciones import ExcepcionFabrica

@dataclass
class FabricaRepositorio(Fabrica):
    def crear_objeto(self, obj: type, mapeador: any = None) -> Repositorio:
        if obj == RepositorioImagenesAnonimizadas:
            return RepositorioImagenesAnonimizadasSQLite()
        elif obj == RepositorioProcesosAnonimizacion:
            return RepositorioProcesosAnonimizacionSQLite()
        else:
            raise ExcepcionFabrica(f"No existe una implementación para el repositorio con el tipo dado: {obj}")