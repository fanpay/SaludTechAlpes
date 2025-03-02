import pulsar,_pulsar  
from pulsar.schema import *
import uuid
import time
import logging
import traceback
import datetime

from saludtech.transformaciones.modulos.anonimizacion.aplicacion.dto import ProcesarImagenDTO
from saludtech.transformaciones.modulos.anonimizacion.aplicacion.servicios import ServicioAnonimizacion
from saludtech.transformaciones.seedwork.infraestructura import utils
from saludtech.transformaciones.modulos.anonimizacion.infraestructura.schema.v1.eventos import EventoAnonimizacionIniciada, EventoAnonimizacionFinalizada, EventoAnonimizacionFinalizadaPayload
from saludtech.transformaciones.modulos.anonimizacion.infraestructura.schema.v1.comandos import ComandoIniciarAnonimizacion
from saludtech.transformaciones.modulos.anonimizacion.aplicacion.comandos.iniciar_anonimizacion import IniciarAnonimizacion
from saludtech.transformaciones.modulos.anonimizacion.infraestructura.despachadores import Despachador
from saludtech.transformaciones.seedwork.aplicacion.comandos import ejecutar_commando
from saludtech.transformaciones.modulos.anonimizacion.infraestructura.schema.v1.eventos import ReferenciaAlmacenamientoPayload

def suscribirse_a_eventos():
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('eventos-transformar12', consumer_type=_pulsar.ConsumerType.Shared,subscription_name='saludtech-sub-eventos', schema=AvroSchema(EventoAnonimizacionIniciada))

        while True:
            mensaje = consumidor.receive()
            evento_integracion = mensaje.value().data
            print(f'------> Evento recibido: {evento_integracion}')

            # Procesar el evento y reaccionar a él
            # Aquí puedes agregar la lógica para manejar el evento recibido

            consumidor.acknowledge(mensaje)

        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de eventos!')
        traceback.print_exc()
        if cliente:
            cliente.close()

def suscribirse_a_comandos():
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('comandos-anonimizacion9', consumer_type=_pulsar.ConsumerType.Shared, subscription_name='saludtech-sub-comandos', schema=AvroSchema(ComandoIniciarAnonimizacion))

        while True:
            mensaje = consumidor.receive()
            comando_integracion = mensaje.value().data
            
            # Transformar el comando de integración en un comando de aplicación
            comando = IniciarAnonimizacion(
                id=comando_integracion.id,
                metadatos=comando_integracion.metadatos,
                configuracion=comando_integracion.configuracion,
                referencia_entrada=comando_integracion.referencia_entrada
            )
            
            
            ejecutar_commando(comando)
            
            evento_finalizado = EventoAnonimizacionFinalizada(
                data = EventoAnonimizacionFinalizadaPayload(
                    id = comando.id,
                    referencia_salida = ReferenciaAlmacenamientoPayload(),
                    timestamp = int(datetime.datetime.now().timestamp())
                )
            )
            despachador = Despachador()
            despachador.publicar_evento(evento_finalizado, 'eventos-enriquecer')

            consumidor.acknowledge(mensaje)
            
        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de comandos!')
        traceback.print_exc()
        if cliente:
            cliente.close()