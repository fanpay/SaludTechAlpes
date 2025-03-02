import pulsar
from pulsar.schema import *

from saludtech.transformaciones.modulos.anonimizacion.infraestructura.schema.v1.eventos import EventoAnonimizacionFallidaPayload, EventoAnonimizacionFinalizadaPayload, EventoAnonimizacionIniciada, EventoAnonimizacionFinalizada, EventoAnonimizacionFallida, EventoAnonimizacionIniciadaPayload
from saludtech.transformaciones.modulos.anonimizacion.infraestructura.schema.v1.comandos import AjusteContrastePayload, ComandoIniciarAnonimizacion, ComandoIniciarAnonimizacionPayload, ConfiguracionAnonimizacionPayload, MetadatosImagenPayload, ReferenciaAlmacenamientoPayload, ResolucionPayload
from saludtech.transformaciones.seedwork.infraestructura import utils
from saludtech.transformaciones.seedwork.infraestructura.despachadores import DespachadorBase, publicar_mensaje
from saludtech.transformaciones.modulos.anonimizacion.aplicacion.comandos.iniciar_anonimizacion import IniciarAnonimizacion

import datetime

epoch = datetime.datetime.utcfromtimestamp(0)

def unix_time_millis(dt):
    return (dt - epoch).total_seconds() * 1000.0

class Despachador(DespachadorBase):
    def _publicar_mensaje(self, mensaje, topico, schema):
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        publicador = cliente.create_producer(topico, schema=schema)
        publicador.send(mensaje)
        cliente.close()

    def publicar_evento(self, evento, topico):
        if isinstance(evento, EventoAnonimizacionIniciada):
            payload = EventoAnonimizacionIniciadaPayload(
                id=str(evento.id),
                metadatos=evento.metadatos,
                configuracion=evento.configuracion,
                referencia_entrada=evento.referencia_entrada,
                timestamp=int(unix_time_millis(evento.timestamp))
            )
            evento_integracion = EventoAnonimizacionIniciada(data=payload)
            self._publicar_mensaje(evento_integracion, topico, AvroSchema(EventoAnonimizacionIniciada))
        elif isinstance(evento, EventoAnonimizacionFinalizada):
            payload = EventoAnonimizacionFinalizadaPayload(
                id=str(evento.data.id),
                referencia_salida=evento.data.referencia_salida,
                timestamp=int(datetime.datetime.now().timestamp())
            )
            evento_integracion = EventoAnonimizacionFinalizada(data=payload)
            self._publicar_mensaje(evento_integracion, topico, AvroSchema(EventoAnonimizacionFinalizada))
        elif isinstance(evento, EventoAnonimizacionFallida):
            payload = EventoAnonimizacionFallidaPayload(
                id=str(evento.id),
                motivo_fallo=evento.motivo_fallo,
                timestamp=int(unix_time_millis(evento.timestamp))
            )
            evento_integracion = EventoAnonimizacionFallida(data=payload)
            self._publicar_mensaje(evento_integracion, topico, AvroSchema(EventoAnonimizacionFallida))

    
    def publicar_comando(self, comando, topico):
        publicar_mensaje(comando, topico)

@publicar_mensaje.register
def _(comando: IniciarAnonimizacion, topico):
    
    payload = ComandoIniciarAnonimizacionPayload(
        id=str(comando.id),
        metadatos=MetadatosImagenPayload(
            id=str(comando.id),
            modalidad=comando.metadatos.modalidad,
            region=comando.metadatos.region,
            resolucion=str(comando.metadatos.resolucion),
            fecha_adquisicion=comando.metadatos.fecha_adquisicion
        ),
        configuracion=ConfiguracionAnonimizacionPayload(
            id=str(comando.id),
            nivel_anonimizacion = comando.configuracion.nivel_anonimizacion,
            formato_salida = comando.configuracion.formato_salida,
            ajustes_contraste = str(comando.configuracion.ajustes_contraste),
            algoritmo = comando.configuracion.algoritmo,
        ),
        referencia_entrada=ReferenciaAlmacenamientoPayload(
            id=str(comando.id),
            nombre_bucket = comando.referencia_entrada.nombre_bucket,
            llave_objeto = comando.referencia_entrada.llave_objeto,
            proveedor_almacenamiento = comando.referencia_entrada.proveedor_almacenamiento
        )
    )
    comando_integracion = ComandoIniciarAnonimizacion(data=payload)
    despachador = Despachador()
    despachador._publicar_mensaje(comando_integracion, topico, AvroSchema(ComandoIniciarAnonimizacion))
