from pulsar.schema import *
from saludtech.transformaciones.seedwork.infraestructura.schema.v1.eventos import EventoIntegracion

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

class EventoAnonimizacionIniciadaPayload(Record):
    id = String()
    metadatos = MetadatosImagenPayload()
    configuracion = ConfiguracionAnonimizacionPayload()
    referencia_entrada = ReferenciaAlmacenamientoPayload()
    timestamp = Long()

class EventoAnonimizacionIniciada(EventoIntegracion):
    data = EventoAnonimizacionIniciadaPayload()

class EventoAnonimizacionFinalizadaPayload(Record):
    id = String()
    referencia_salida = ReferenciaAlmacenamientoPayload()
    timestamp = Long()

class EventoAnonimizacionFinalizada(EventoIntegracion):
    data = EventoAnonimizacionFinalizadaPayload()

class EventoAnonimizacionFallidaPayload(Record):
    id = String()
    motivo_fallo = String()
    timestamp = Long()

class EventoAnonimizacionFallida(EventoIntegracion):
    data = EventoAnonimizacionFallidaPayload()