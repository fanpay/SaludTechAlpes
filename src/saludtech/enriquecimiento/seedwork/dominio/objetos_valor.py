"""Objetos valor reusables parte del seedwork del proyecto

En este archivo usted encontrará los objetos valor reusables parte del seedwork del proyecto

"""

from dataclasses import dataclass
from abc import ABC, abstractmethod
from .entidades import Locacion
from datetime import datetime

@dataclass(frozen=True)
class ObjetoValor:
    ...

@dataclass(frozen=True)
class Codigo(ABC, ObjetoValor):
    """Código único que puede aplicarse a cualquier entidad u objeto de valor"""
    codigo: str


@dataclass(frozen=True)
class Resolucion(ObjetoValor):
    """Resolución de imágenes (puede reutilizarse en cualquier dominio de procesamiento gráfico)"""
    ancho: int
    alto: int
    dpi: int


@dataclass(frozen=True)
class AjusteContraste(ObjetoValor):
    brillo: float
    contraste: float
    