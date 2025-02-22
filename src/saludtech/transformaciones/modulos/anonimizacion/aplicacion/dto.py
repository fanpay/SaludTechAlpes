from dataclasses import dataclass, field
from saludtech.transformaciones.seedwork.aplicacion.dto import DTO
from datetime import datetime

    

@dataclass(frozen=True)
class MetadatosImagenDTO(DTO):
    modalidad: str
    region: str
    resolucion: str
    fecha_adquisicion: datetime

@dataclass(frozen=True)
class ConfiguracionAnonimizacionDTO(DTO):
    nivel_anonimizacion: int
    formato_salida: str
    ajustes_contraste: dict
    algoritmo: str

@dataclass(frozen=True)
class ResultadoProcesamientoDTO(DTO):
    checksum: str
    tamano_archivo: int
    timestamp: datetime = field(default_factory=datetime.now)
    

@dataclass(frozen=True)
class ReferenciaAlmacenamientoDTO(DTO):
    nombre_bucket: str
    llave_objeto: str
    proveedor_almacenamiento: str

@dataclass(frozen=True)
class ImagenAnonimizadaDTO(DTO):
    id: str
    metadatos: MetadatosImagenDTO
    configuracion: ConfiguracionAnonimizacionDTO
    referencia_entrada: ReferenciaAlmacenamientoDTO
    referencia_salida: ReferenciaAlmacenamientoDTO
    estado: str
    resultado: str
    fecha_solicitud: str = field(default_factory=str)  # Fecha de solicitud de anonimización

