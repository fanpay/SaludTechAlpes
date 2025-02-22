from pulsar.schema import *
from dataclasses import dataclass, field
from aeroalpes.seedwork.infraestructura.schema.v1.comandos import (ComandoIntegracion)


class AeropuertoPayload(Record):
    codigo = String()
    nombre = String()

class LegPayload(Record):
    fecha_salida = String()
    fecha_llegada = String()
    origen = AeropuertoPayload()
    destino = AeropuertoPayload()

class SegmentoPayload(Record):
    legs = Array(LegPayload())

class OdoPayload(Record):
    segmentos = Array(SegmentoPayload())

class ItinerarioPayload(Record):
    odos = Array(OdoPayload())

class ComandoCrearReservaPayload(ComandoIntegracion):
    id_usuario = String()
    fecha_creacion = String()
    fecha_actualizacion = String()
    itinerarios = Array(ItinerarioPayload())

'''class ComandoCrearReservaPayload(ComandoIntegracion):
    id_usuario = String()
    # TODO Cree los records para itinerarios'''

class ComandoCrearReserva(ComandoIntegracion):
    data = ComandoCrearReservaPayload()