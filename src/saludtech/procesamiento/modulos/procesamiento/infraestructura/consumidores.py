import pulsar,_pulsar  
from pulsar.schema import *
import uuid
import time
import logging
import traceback
import datetime

from saludtech.procesamiento.modulos.procesamiento.aplicacion.dto import ProcesarImagenDTO
from saludtech.procesamiento.modulos.procesamiento.aplicacion.servicios import ServicioAnonimizacion
from saludtech.procesamiento.seedwork.infraestructura import utils
from saludtech.procesamiento.modulos.procesamiento.infraestructura.schema.v1.eventos import ConfiguracionAnonimizacionPayload, EventoAnonimizacion, EventoAnonimizacionPayload, MetadatosImagenPayload, AjusteContrastePayload, ResolucionPayload
from saludtech.procesamiento.modulos.procesamiento.infraestructura.schema.v1.comandos import ComandoIniciarAnonimizacion
from saludtech.procesamiento.modulos.procesamiento.aplicacion.comandos.iniciar_anonimizacion import IniciarAnonimizacion
from saludtech.procesamiento.modulos.procesamiento.infraestructura.despachadores import Despachador
from saludtech.procesamiento.seedwork.aplicacion.comandos import ejecutar_commando
from saludtech.procesamiento.modulos.procesamiento.infraestructura.schema.v1.eventos import ReferenciaAlmacenamientoPayload

def suscribirse_a_eventos():
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('eventos-procesar6', consumer_type=_pulsar.ConsumerType.Shared,subscription_name='saludtech-sub-eventos', schema=AvroSchema(EventoAnonimizacion))

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
        consumidor = cliente.subscribe('comandos-procesamiento5', consumer_type=_pulsar.ConsumerType.Shared, subscription_name='saludtech-sub-comandos', schema=AvroSchema(ComandoIniciarAnonimizacion))

        while True:
            
            mensaje = consumidor.receive()
            comando_integracion = mensaje.value().data
            # Transformar el comando de integración en un comando de aplicación
            comando = IniciarAnonimizacion(
                id=comando_integracion.id,
                nombre=comando_integracion.nombre,
                cedula=comando_integracion.cedula,
                metadatos=comando_integracion.metadatos,
                configuracion=comando_integracion.configuracion,
                usuario=comando_integracion.usuario,
                id_solicitud = comando_integracion.id_solicitud,
                referencia_entrada=comando_integracion.referencia_entrada
            )
            
            
            ejecutar_commando(comando)
            
            evento = EventoAnonimizacion(
                data = EventoAnonimizacionPayload(
                    id = comando.id_solicitud,
                    nombre_paciente = comando.nombre,
                    cedula = comando.cedula,
                    configuracion = ConfiguracionAnonimizacionPayload(
                        id = comando.configuracion.id,
                        nivel_anonimizacion = comando.configuracion.nivel_anonimizacion,
                        formato_salida = comando.configuracion.formato_salida,
                        ajustes_contraste = AjusteContrastePayload(
                            brillo = comando.configuracion.ajustes_contraste.brillo,
                            contraste = comando.configuracion.ajustes_contraste.contraste
                        ),
                        algoritmo = comando.configuracion.algoritmo
                        ),
                    metadatos = MetadatosImagenPayload(
                        id = comando.metadatos.id,
                        modalidad = comando.metadatos.modalidad,
                        region = comando.metadatos.region,
                        resolucion = ResolucionPayload(
                            alto=comando.metadatos.resolucion.alto,
                            ancho=comando.metadatos.resolucion.ancho,
                            dpi=comando.metadatos.resolucion.dpi
                            ),
                        fecha_adquisicion = comando.metadatos.fecha_adquisicion,
                        ),
                    referencia_entrada = ReferenciaAlmacenamientoPayload(
                         id = comando.referencia_entrada.id, 
                         nombre_bucket = comando.referencia_entrada.nombre_bucket,
                         llave_objeto = comando.referencia_entrada.llave_objeto,
                         proveedor_almacenamiento = comando.referencia_entrada.proveedor_almacenamiento
                        ),
                    timestamp = int(datetime.datetime.now().timestamp())
                )
            )
            despachador = Despachador()
            despachador.publicar_evento(evento, 'eventos-transformar7')

            consumidor.acknowledge(mensaje)
            
        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de comandos!')
        traceback.print_exc()
        if cliente:
            cliente.close()