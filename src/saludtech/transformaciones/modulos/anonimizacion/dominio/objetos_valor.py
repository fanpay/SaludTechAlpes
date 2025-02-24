from __future__ import annotations

from dataclasses import dataclass, field
from saludtech.transformaciones.seedwork.dominio.objetos_valor import ObjetoValor, Resolucion, AjusteContraste
from datetime import datetime
from enum import Enum


# ENUMS
class ModalidadImagen(str, Enum):
    RAYOS_X = "RayosX"
    RESONANCIA = "ResonanciaMagnética"
    TOMOGRAFIA = "Tomografía"
    ULTRASONIDO = "Ultrasonido"
    MAMOGRAFIA = "Mamografía"
    HISTOPATOLOGIA = "Histopatología"

class RegionAnatomica(str, Enum):
    CABEZA_CUELLO = "CabezaYCuello"
    TORAX = "Tórax"
    ABDOMEN = "Abdomen"
    MUSCULOESQUELETICO = "Musculoesquelético"
    PELVIS = "Pélvis"
    CUERPO_COMPLETO = "CuerpoCompleto"

class FormatoSalida(str, Enum):
    DICOM = "DICOM"
    NIFTI = "NIfTI"
    PNG = "PNG"
    JPEG = "JPEG"

class EstadoProceso(str, Enum):
    EXITOSO = "EXITOSO"
    FALLIDO = "FALLIDO"
    PENDIENTE = "PENDIENTE"
    PROCESANDO = "PROCESANDO"
    
class AlgoritmoAnonimizacion(str, Enum):
    DICOM_DEID = "DICOM_DEID"
    PIXEL_SCRAMBLE = "PIXEL_SCRAMBLE"
    MASK_REGIONS = "MASK_REGIONS"
    
# OBJETOS DE VALOR

@dataclass(frozen=True)
class MetadatosImagen:
    modalidad: ModalidadImagen
    region: RegionAnatomica
    resolucion: Resolucion
    fecha_adquisicion: datetime

@dataclass(frozen=True)
class ConfiguracionAnonimizacion:
    nivel_anonimizacion: int  # 1-5
    formato_salida: FormatoSalida  # DICOM, NIfTI, etc.
    ajustes_contraste: AjusteContraste  # {brillo: 1.2, contraste: 0.8}
    algoritmo: AlgoritmoAnonimizacion

@dataclass(frozen=True)
class ResultadoProcesamiento:
    checksum: str
    tamano_archivo: int  # bytes
    timestamp: datetime = datetime.now()
    
@dataclass(frozen=True)
class ReferenciaAlmacenamiento(ObjetoValor):
    nombre_bucket: str
    llave_objeto: str
    proveedor_almacenamiento: str  # "S3", "GCS", etc.
    
