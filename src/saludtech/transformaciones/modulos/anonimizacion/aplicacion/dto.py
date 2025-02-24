from dataclasses import dataclass, field
from typing import Optional
from saludtech.transformaciones.modulos.anonimizacion.dominio.objetos_valor import AlgoritmoAnonimizacion, EstadoProceso, FormatoSalida, ModalidadImagen, RegionAnatomica
from saludtech.transformaciones.seedwork.aplicacion.dto import DTO
from datetime import datetime

from saludtech.transformaciones.seedwork.dominio.objetos_valor import Resolucion

@dataclass(frozen=True)
class ResolucionDTO(DTO):
    ancho: int
    alto: int
    dpi: int   
@dataclass(frozen=True)
class AjusteContrasteDTO(DTO):
    brillo: float
    contraste: float    

@dataclass(frozen=True)
class MetadatosImagenDTO(DTO):
    modalidad: ModalidadImagen
    region: RegionAnatomica
    resolucion: Resolucion
    fecha_adquisicion: datetime

@dataclass(frozen=True)
class ConfiguracionAnonimizacionDTO(DTO):
    nivel_anonimizacion: int
    formato_salida: FormatoSalida
    ajustes_contraste: AjusteContrasteDTO
    algoritmo_usado: AlgoritmoAnonimizacion

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

# ====================
# COMANDOS (Escritura)
# ====================
@dataclass(frozen=True)
class ProcesarImagenDTO(DTO):
    metadatos: MetadatosImagenDTO
    configuracion: ConfiguracionAnonimizacionDTO
    referencia_entrada: ReferenciaAlmacenamientoDTO

# =================
# QUERIES (Lectura)
# =================
@dataclass(frozen=True)
class EstadoProcesoDTO(DTO):
    id: str
    estado: EstadoProceso
    metadatos: MetadatosImagenDTO
    referencia_entrada: ReferenciaAlmacenamientoDTO
    referencia_salida: Optional[ReferenciaAlmacenamientoDTO]
    resultado: Optional[ResultadoProcesamientoDTO]
    fecha_solicitud: datetime
    fecha_ultima_actualizacion: datetime
    error: Optional[str] = None