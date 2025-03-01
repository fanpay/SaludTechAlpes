""" Fábricas para la creación de objetos del dominio de anonimización """

from .entidades import Imagen
from .reglas import (
    ImagenDebeTenerReferencia,
    ImagenDebeSerProcesable,
    NivelAnonimizacionValido,
    FormatoImagenSoportado
)
from .excepciones import TipoObjetoNoExisteEnDominioAnonimizacionExcepcion
from saludtech.procesamiento.seedwork.dominio.repositorios import Mapeador, Repositorio
from saludtech.procesamiento.seedwork.dominio.fabricas import Fabrica
from saludtech.procesamiento.seedwork.dominio.entidades import Entidad
from dataclasses import dataclass

@dataclass
class _FabricaImagen(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if isinstance(obj, Entidad):
            return mapeador.entidad_a_dto(obj)
        else:
            imagen: Imagen = mapeador.dto_a_entidad(obj)
            
            # Validar reglas de negocio críticas
            self.validar_regla(ImagenDebeTenerReferencia(imagen.referencia_entrada))
            self.validar_regla(ImagenDebeSerProcesable(imagen))
            self.validar_regla(NivelAnonimizacionValido(imagen.configuracion))
            self.validar_regla(FormatoImagenSoportado(imagen.configuracion))

            
            return imagen

@dataclass
class FabricaAnonimizacion(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if mapeador.obtener_tipo() == Imagen.__class__:
            fabrica_imagen = _FabricaImagen()
            return fabrica_imagen.crear_objeto(obj, mapeador)
        else:
            raise TipoObjetoNoExisteEnDominioAnonimizacionExcepcion()