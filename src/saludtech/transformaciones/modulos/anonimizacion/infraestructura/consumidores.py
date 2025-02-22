import pulsar,_pulsar  
from pulsar.schema import *
import uuid
import time
import logging
import traceback

from aeroalpes.modulos.vuelos.infraestructura.schema.v1.eventos import EventoReservaCreada
from aeroalpes.modulos.vuelos.infraestructura.schema.v1.comandos import ComandoCrearReserva
from aeroalpes.seedwork.infraestructura import utils
from aeroalpes.modulos.vuelos.aplicacion.comandos.crear_reserva import CrearReserva
from aeroalpes.modulos.vuelos.infraestructura.despachadores import Despachador

def suscribirse_a_eventos():
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('eventos-reserva1', consumer_type=_pulsar.ConsumerType.Shared,subscription_name='aeroalpes-sub-eventos', schema=AvroSchema(EventoReservaCreada))

        while True:
            mensaje = consumidor.receive()
            evento_integracion = mensaje.value().data
            print(f'Evento recibido: {evento_integracion}')

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
        consumidor = cliente.subscribe('comandos-reserva5', consumer_type=_pulsar.ConsumerType.Shared, subscription_name='aeroalpes-sub-comandos', schema=AvroSchema(ComandoCrearReserva))

        while True:
            mensaje = consumidor.receive()
            comando_integracion = mensaje.value().data
            print(f'Comando recibido v2: {comando_integracion}')

            # Transformar el comando de integración en un comando de aplicación
            comando = CrearReserva(
                fecha_creacion=comando_integracion.fecha_creacion,
                fecha_actualizacion=comando_integracion.fecha_actualizacion,
                id=comando_integracion.id_usuario,
                itinerarios=comando_integracion.itinerarios
            )

            # Usar el despachador para manejar el comando
            despachador = Despachador()
            despachador.publicar_comando(comando, 'comandos-reservas')

            consumidor.acknowledge(mensaje)
            
        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de comandos!')
        traceback.print_exc()
        if cliente:
            cliente.close()