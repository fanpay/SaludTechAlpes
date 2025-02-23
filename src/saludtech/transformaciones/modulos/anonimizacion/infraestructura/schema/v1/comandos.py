from pulsar.schema import *
from dataclasses import dataclass, field
from saludtech.transformaciones.seedwork.infraestructura.schema.v1.comandos import ComandoIntegracion

class MetadatosImagenPayload(Record):
    id = String()
    modalidad = String()
    region = String()
    resolucion = String()
    fecha_adquisicion = String()

class ConfiguracionAnonimizacionPayload(Record):
    id = String()
    nivel_anonimizacion = String()
    formato_salida = String()
    ajustes_contraste = String()
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