""" Fábricas para la creación de objetos del dominio de anonimización """

from .entidades import ImagenAnonimizada
from .reglas import (
    ImagenDebeTenerReferencia,
    ImagenDebeSerProcesable,
    NivelAnonimizacionValido,
    FormatoImagenSoportado
)
from .excepciones import TipoObjetoNoExisteEnDominioAnonimizacionExcepcion
from saludtech.transformaciones.seedwork.dominio.repositorios import Mapeador, Repositorio
from saludtech.transformaciones.seedwork.dominio.fabricas import Fabrica
from saludtech.transformaciones.seedwork.dominio.entidades import Entidad
from dataclasses import dataclass

@dataclass
class _FabricaImagenAnonimizada(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if isinstance(obj, Entidad):
            return mapeador.entidad_a_dto(obj)
        else:
            imagen: ImagenAnonimizada = mapeador.dto_a_entidad(obj)
            
            # Validar reglas de negocio críticas
            self.validar_regla(ImagenDebeTenerReferencia(imagen.referencia_entrada))
            #self.validar_regla(ImagenDebeSerProcesable(imagen))
            self.validar_regla(NivelAnonimizacionValido(imagen.configuracion))
            self.validar_regla(FormatoImagenSoportado(imagen.configuracion))

            
            return imagen

@dataclass
class FabricaAnonimizacion(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if mapeador.obtener_tipo() == ImagenAnonimizada.__class__:
            fabrica_imagen = _FabricaImagenAnonimizada()
            return fabrica_imagen.crear_objeto(obj, mapeador)
        else:
            raise TipoObjetoNoExisteEnDominioAnonimizacionExcepcion()