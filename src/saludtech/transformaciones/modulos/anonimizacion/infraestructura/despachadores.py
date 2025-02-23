import pulsar
from pulsar.schema import *

from saludtech.transformaciones.modulos.anonimizacion.infraestructura.schema.v1.eventos import EventoAnonimizacionFallidaPayload, EventoAnonimizacionFinalizadaPayload, EventoAnonimizacionIniciada, EventoAnonimizacionFinalizada, EventoAnonimizacionFallida, EventoAnonimizacionIniciadaPayload
from saludtech.transformaciones.modulos.anonimizacion.infraestructura.schema.v1.comandos import ComandoIniciarAnonimizacion, ComandoIniciarAnonimizacionPayload
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
        publicador = cliente.create_producer(topico, schema=AvroSchema(ComandoIniciarAnonimizacion))
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
                id=str(evento.id),
                referencia_salida=evento.referencia_salida,
                timestamp=int(unix_time_millis(evento.timestamp))
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
        metadatos=comando.metadatos,
        configuracion=comando.configuracion,
        referencia_entrada=comando.referencia_entrada
    )
    comando_integracion = ComandoIniciarAnonimizacion(data=payload)
    despachador = Despachador()
    despachador._publicar_mensaje(comando_integracion, topico, AvroSchema(ComandoIniciarAnonimizacion))
