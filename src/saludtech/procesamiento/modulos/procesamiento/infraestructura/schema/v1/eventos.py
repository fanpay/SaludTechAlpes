from pulsar.schema import *
from saludtech.procesamiento.seedwork.infraestructura.schema.v1.eventos import EventoIntegracion

class ResolucionPayload(Record):
    alto = Integer()
    ancho = Integer()
    dpi = Integer()

class MetadatosImagenPayload(Record):
    id = String()
    modalidad = String()
    region = String()
    resolucion = String()
    fecha_adquisicion = String()

class AjusteContrastePayload(Record):
    brillo = Integer()
    contraste = Integer()


class ConfiguracionAnonimizacionPayload(Record):
    id = String()
    nivel_anonimizacion = Integer()
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
    nombre_paciente = String()
    cedula = Integer()
    configuracion = ConfiguracionAnonimizacionPayload()
    metadatos = MetadatosImagenPayload()
    referencia_entrada = ReferenciaAlmacenamientoPayload()
    timestamp = Long()

class EventoAnonimizacionIniciada(EventoIntegracion):
    data = EventoAnonimizacionIniciadaPayload()

class EventoAnonimizacionPayload(Record):
    id = String()
    nombre_paciente = String()
    cedula = Integer()
    configuracion = ConfiguracionAnonimizacionPayload()
    metadatos = MetadatosImagenPayload()
    referencia_entrada = ReferenciaAlmacenamientoPayload()
    timestamp = Long()

class EventoAnonimizacion(EventoIntegracion):
    data = EventoAnonimizacionPayload()

class EventoAnonimizacionFallidaPayload(Record):
    id = String()
    motivo_fallo = String()
    timestamp = Long()

class EventoAnonimizacionFallida(EventoIntegracion):
    data = EventoAnonimizacionFallidaPayload()