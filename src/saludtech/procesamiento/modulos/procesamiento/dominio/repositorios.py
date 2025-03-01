""" Interfaces para los repositorios del dominio de anonimización de imágenes.

En este archivo se definen las interfaces para los repositorios
que manejarán el almacenamiento y recuperación de entidades en el dominio de anonimización.

"""

from abc import ABC
from saludtech.procesamiento.seedwork.dominio.repositorios import Repositorio

class RepositorioImagenes(Repositorio, ABC):
    """Interfaz para el repositorio de imágenes ."""
    ...

class RepositorioProcesosAnonimizacion(Repositorio, ABC):
    """Interfaz para el repositorio de procesos de anonimización."""
    ...
