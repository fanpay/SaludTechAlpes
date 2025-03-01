"""Entidades del dominio de anonimizacion

En este archivo usted encontrará las entidades del dominio de anonimizacion

"""

from __future__ import annotations
from dataclasses import dataclass, field
import uuid
import datetime

from saludtech.transformaciones.modulos.anonimizacion.dominio.objetos_valor import ConfiguracionAnonimizacion, MetadatosImagen, ResultadoProcesamiento, ReferenciaAlmacenamiento, EstadoProceso
from saludtech.transformaciones.modulos.anonimizacion.dominio.eventos import ProcesoAnonimizacionIniciado, ProcesoAnonimizacionFinalizado, ProcesoAnonimizacionFallido
from saludtech.transformaciones.seedwork.dominio.entidades import AgregacionRaiz, Entidad

@dataclass
class ImagenAnonimizada(AgregacionRaiz):
    metadatos: MetadatosImagen = field(default_factory=MetadatosImagen)
    configuracion: ConfiguracionAnonimizacion = field(default_factory=ConfiguracionAnonimizacion)
    referencia_entrada: ReferenciaAlmacenamiento = field(default_factory=ReferenciaAlmacenamiento) # Ubicación de la imagen original
    referencia_salida: ReferenciaAlmacenamiento = field(default_factory=ReferenciaAlmacenamiento)
    estado: EstadoProceso = field(default=EstadoProceso.PENDIENTE)   # PENDING, PROCESSING, COMPLETED, FAILED
    #resultado: ResultadoProcesamiento = field(default_factory=ResultadoProcesamiento)
    fecha_solicitud:  datetime.datetime = field(default_factory=datetime.datetime.now)

    def iniciar_procesamiento(self, imagen: ImagenAnonimizada):
        self.estado = EstadoProceso.PROCESANDO
        self.metadatos = imagen.metadatos
        self.referencia_entrada = imagen.referencia_entrada
        self.configuracion = imagen.configuracion
        
        
        self.agregar_evento(ProcesoAnonimizacionIniciado(
            metadatos=self.metadatos,
            referencia_entrada=self.referencia_entrada,
            configuracion=self.configuracion
        ))

    def completar_exitosamente(self, referencia_salida: ReferenciaAlmacenamiento):
        self.referencia_salida = referencia_salida
        self.estado = EstadoProceso.EXITOSO
        self.agregar_evento(ProcesoAnonimizacionFinalizado(
            proceso_id=self.id,
            referencia_salida=referencia_salida,
            metadatos=self.metadatos
        ))

    def marcar_fallido(self, motivo_fallo: str):
        self.estado = EstadoProceso.FALLIDO
        self.agregar_evento(ProcesoAnonimizacionFallido(
            proceso_id=self.id,
            motivo_fallo=motivo_fallo,
            metadatos=self.metadatos,
            referencia_entrada=self.referencia_entrada
        ))


@dataclass
class SolicitudAnonimizacion(Entidad):
    id_solicitud: uuid.UUID = field(hash=True, default=None)
    id_imagen: uuid.UUID = field(hash=True, default=None)
    configuracion: ConfiguracionAnonimizacion = None