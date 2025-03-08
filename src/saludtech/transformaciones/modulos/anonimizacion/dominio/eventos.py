from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
import uuid
from saludtech.transformaciones.seedwork.dominio.eventos import EventoDominio
from .objetos_valor import ReferenciaAlmacenamiento, MetadatosImagen, ConfiguracionAnonimizacion
from datetime import datetime, timezone


@dataclass
class ProcesoAnonimizacionIniciado(EventoDominio):
    """Evento que indica que el proceso de anonimización ha iniciado."""
    proceso_id: uuid.UUID = None
    metadatos: MetadatosImagen = None
    referencia_entrada: ReferenciaAlmacenamiento = None
    configuracion: ConfiguracionAnonimizacion = None
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class ProcesoAnonimizacionFinalizado(EventoDominio):
    """Evento que indica que el proceso de anonimización ha finalizado exitosamente."""
    proceso_id: uuid.UUID = None
    referencia_salida: ReferenciaAlmacenamiento = None
    metadatos: MetadatosImagen = None
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class ProcesoAnonimizacionFallido(EventoDominio):
    """Evento que indica que el proceso de anonimización falló."""
    proceso_id: uuid.UUID = None
    motivo_fallo: str = ""
    metadatos: MetadatosImagen = None
    referencia_entrada: ReferenciaAlmacenamiento = None
    fecha_fallo: datetime = datetime.now(timezone.utc)



@dataclass
class MetadataEnriquecimientoRequerido(EventoDominio):
    imagen_id: uuid.UUID = None
    referencia_procesada: ReferenciaAlmacenamiento = None
    metadatos_actuales: MetadatosImagen = None
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class MetadataEnriquecida(EventoDominio):
    imagen_id: uuid.UUID = None
    metadatos_enriquecidos: MetadatosImagen = None
    referencia_final: ReferenciaAlmacenamiento = None
    timestamp: datetime = field(default_factory=datetime.now)