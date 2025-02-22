import pulsar
from pulsar.schema import *

from aeroalpes.modulos.vuelos.infraestructura.schema.v1.eventos import EventoReservaCreada, ReservaCreadaPayload
from aeroalpes.modulos.vuelos.infraestructura.schema.v1.comandos import ComandoCrearReserva, ComandoCrearReservaPayload, AeropuertoPayload
from aeroalpes.seedwork.infraestructura import utils
from aeroalpes.seedwork.infraestructura.despachadores import DespachadorBase, publicar_mensaje
from aeroalpes.modulos.vuelos.aplicacion.comandos.crear_reserva import CrearReserva

import datetime

epoch = datetime.datetime.utcfromtimestamp(0)

def unix_time_millis(dt):
    return (dt - epoch).total_seconds() * 1000.0

class Despachador(DespachadorBase):
    def _publicar_mensaje(self, mensaje, topico, schema):
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        publicador = cliente.create_producer(topico, schema=AvroSchema(ComandoCrearReserva))
        publicador.send(mensaje)
        cliente.close()

    def publicar_evento(self, evento, topico):
        # TODO Debe existir un forma de crear el Payload en Avro con base al tipo del evento
        payload = ReservaCreadaPayload(
            id_reserva=str(evento.id_reserva), 
            id_cliente=str(evento.id_cliente), 
            estado=str(evento.estado), 
            fecha_creacion=int(unix_time_millis(evento.fecha_creacion))
        )
        evento_integracion = EventoReservaCreada(data=payload)
        self._publicar_mensaje(evento_integracion, topico, AvroSchema(EventoReservaCreada))
    
    def publicar_comando(self, comando, topico):
        publicar_mensaje(comando, topico)

@publicar_mensaje.register
def _(comando: CrearReserva, topico):
    itinerarios_payload = [
        {
            'odos': [
                {
                    'segmentos': [
                        {
                            'legs': [
                                {
                                    'fecha_salida': leg.fecha_salida,
                                    'fecha_llegada': leg.fecha_llegada,
                                    'origen': {
                                        'codigo': leg.origen['codigo'] if isinstance(leg.origen, dict) else leg.origen.codigo,
                                        'nombre': leg.origen['nombre'] if isinstance(leg.origen, dict) else leg.origen.nombre
                                    },
                                    'destino': {
                                        'codigo': leg.destino['codigo'] if isinstance(leg.destino, dict) else leg.destino.codigo,
                                        'nombre': leg.destino['nombre'] if isinstance(leg.destino, dict) else leg.destino.nombre
                                    }
                                } for leg in segmento.legs
                            ]
                        } for segmento in odo.segmentos
                    ]
                } for odo in itinerario.odos
            ]
        } for itinerario in comando.itinerarios
    ]

    payload = ComandoCrearReservaPayload(
        id_usuario=str(comando.id),
        fecha_creacion=comando.fecha_creacion,
        fecha_actualizacion=comando.fecha_actualizacion,
        itinerarios=itinerarios_payload
    )
    comando_integracion = ComandoCrearReserva(data=payload)
    despachador = Despachador()
    despachador._publicar_mensaje(comando_integracion, topico, AvroSchema(ComandoCrearReserva))
