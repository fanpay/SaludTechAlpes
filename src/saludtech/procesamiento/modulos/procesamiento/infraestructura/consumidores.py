import pulsar,_pulsar  
from pulsar.schema import *
import uuid
import time
import logging
import traceback
import datetime

from saludtech.procesamiento.config import db
from saludtech.procesamiento.modulos.procesamiento.aplicacion.dto import ProcesarImagenDTO
from saludtech.procesamiento.modulos.procesamiento.aplicacion.servicios import ServicioAnonimizacion
from saludtech.procesamiento.modulos.procesamiento.dominio.objetos_valor import EstadoProceso
from saludtech.procesamiento.modulos.procesamiento.infraestructura.dto import ImagenDTO
from saludtech.procesamiento.seedwork.infraestructura import utils
from saludtech.procesamiento.modulos.procesamiento.infraestructura.schema.v1.eventos import ConfiguracionAnonimizacionPayload, EventoAnonimizacionFallida, EventoAnonimizacionIniciada, EventoAnonimizacionIniciadaPayload, MetadatosImagenPayload, AjusteContrastePayload, ResolucionPayload
from saludtech.procesamiento.modulos.procesamiento.infraestructura.schema.v1.comandos import ComandoIniciarAnonimizacion
from saludtech.procesamiento.modulos.procesamiento.aplicacion.comandos.iniciar_anonimizacion import IniciarAnonimizacion
from saludtech.procesamiento.modulos.procesamiento.infraestructura.despachadores import Despachador
from saludtech.procesamiento.seedwork.aplicacion.comandos import ejecutar_commando
from saludtech.procesamiento.modulos.procesamiento.infraestructura.schema.v1.eventos import ReferenciaAlmacenamientoPayload

MS_NO_PROCESADO = "no procesado"

def suscribirse_a_eventos():
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('eventos-anonimizacion-fallida', consumer_type=_pulsar.ConsumerType.Shared,subscription_name='saludtech-sub-eventos', schema=AvroSchema(EventoAnonimizacionFallida))

        while True:
            mensaje = consumidor.receive()
            evento_integracion = mensaje.value().data
            print(f'------> Evento recibido: {evento_integracion}')
            id = evento_integracion.id
            imagen_anonimizada = db.session.query(ImagenDTO).filter_by(id_solicitud=id).first()

            print(f'---> Buscando entidad con ID: {str(id)} o la siguiente {id}')

            if imagen_anonimizada:
                # Actualizar la entidad y los metadatos
                imagen_anonimizada.estado = EstadoProceso.FALLIDO
                imagen_anonimizada.metadatos.modalidad = MS_NO_PROCESADO
                imagen_anonimizada.metadatos.region = MS_NO_PROCESADO
                imagen_anonimizada.metadatos.resolucion = MS_NO_PROCESADO

                db.session.commit()
                print(f'---> Entidad actualizada por Saga con ID: {id}')
            else:
                print(f'---> No se encontró la entidad con ID: {id}')

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
        consumidor = cliente.subscribe('comandos-procesamiento7', consumer_type=_pulsar.ConsumerType.Shared, subscription_name='saludtech-sub-comandos', schema=AvroSchema(ComandoIniciarAnonimizacion))

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
            
            evento = EventoAnonimizacionIniciada(
                data = EventoAnonimizacionIniciadaPayload(
                    id = comando.id_solicitud,
                    nombre_paciente = comando.nombre,
                    cedula = comando.cedula,
                    configuracion = ConfiguracionAnonimizacionPayload(
                        id = comando.configuracion.id,
                        nivel_anonimizacion = comando.configuracion.nivel_anonimizacion,
                        formato_salida = comando.configuracion.formato_salida,
                        ajustes_contraste = str(comando.configuracion.ajustes_contraste),
                        algoritmo = comando.configuracion.algoritmo
                        ),
                    metadatos = MetadatosImagenPayload(
                        id = comando.metadatos.id,
                        modalidad = comando.metadatos.modalidad,
                        region = comando.metadatos.region,
                        resolucion = str(comando.metadatos.resolucion),
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
            despachador.publicar_evento(evento, 'eventos-transformar12')

            consumidor.acknowledge(mensaje)
            
        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de comandos!')
        traceback.print_exc()
        if cliente:
            cliente.close()