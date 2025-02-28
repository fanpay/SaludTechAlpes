""" Fábricas para la creación de objetos en la capa de infrastructura del dominio de anonimizacion

En este archivo usted encontrará las diferentes fábricas para crear
objetos complejos en la capa de infraestructura del dominio de anonimizacion

"""

from dataclasses import dataclass
from saludtech.enriquecimiento.seedwork.dominio.fabricas import Fabrica
from saludtech.enriquecimiento.seedwork.dominio.repositorios import Repositorio
from saludtech.enriquecimiento.modulos.enriquecimineto.dominio.repositorios import RepositorioImagenesAnonimizadas, RepositorioProcesosAnonimizacion
from .repositorios import RepositorioImagenesAnonimizadasDB, RepositorioProcesosAnonimizacionDB
from .excepciones import ExcepcionFabrica

@dataclass
class FabricaRepositorio(Fabrica):
    def crear_objeto(self, obj: type, mapeador: any = None) -> Repositorio:
        #if obj == RepositorioImagenesAnonimizadas:
        return RepositorioImagenesAnonimizadasDB()
        '''elif obj == RepositorioProcesosAnonimizacion:
            return RepositorioProcesosAnonimizacionDB()
        else:
            raise ExcepcionFabrica(f"No existe una implementación para el repositorio con el tipo dado: {obj}")'''