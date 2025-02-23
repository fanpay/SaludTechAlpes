from datetime import datetime
from pulsar.schema import *
from saludtech.transformaciones.seedwork.infraestructura.schema.v1.comandos import ComandoIntegracion

class AjusteContrastePayload(Record):
    brillo: float
    contraste: float    
    
class ResolucionPayload(Record):
    ancho: int
    alto: int
    dpi: int

class MetadatosImagenPayload(Record):
    id = String()
    modalidad = String()
    region = String()
    resolucion = ResolucionPayload()
    fecha_adquisicion = datetime

class ConfiguracionAnonimizacionPayload(Record):
    id = String()
    nivel_anonimizacion = String()
    formato_salida = String()
    ajustes_contraste = AjusteContrastePayload()
    algoritmo = String()

class ReferenciaAlmacenamientoPayload(Record):
    id = String()
    nombre_bucket = String()
    llave_objeto = String()
    proveedor_almacenamiento = String()

class ComandoIniciarAnonimizacionPayload(ComandoIntegracion):
    id = String()
    metadatos = MetadatosImagenPayload()
    configuracion = ConfiguracionAnonimizacionPayload()
    referencia_entrada = ReferenciaAlmacenamientoPayload()

class ComandoIniciarAnonimizacion(ComandoIntegracion):
    data = ComandoIniciarAnonimizacionPayload()