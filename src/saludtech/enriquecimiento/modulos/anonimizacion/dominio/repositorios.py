""" Interfaces para los repositorios del dominio de anonimización de imágenes.

En este archivo se definen las interfaces para los repositorios
que manejarán el almacenamiento y recuperación de entidades en el dominio de anonimización.

"""

from abc import ABC
from saludtech.enriquecimiento.seedwork.dominio.repositorios import Repositorio

class RepositorioImagenesAnonimizadas(Repositorio, ABC):
    """Interfaz para el repositorio de imágenes anonimizadas."""
    ...

class RepositorioProcesosAnonimizacion(Repositorio, ABC):
    """Interfaz para el repositorio de procesos de anonimización."""
    ...
