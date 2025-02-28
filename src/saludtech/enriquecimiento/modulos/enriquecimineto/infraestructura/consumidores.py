import pulsar,_pulsar  
from pulsar.schema import *
import logging
import traceback
import datetime
import random

from saludtech.enriquecimiento.config.db import db
from saludtech.enriquecimiento.modulos.enriquecimineto.dominio.objetos_valor import EstadoProceso, ModalidadImagen, RegionAnatomica
from saludtech.enriquecimiento.modulos.enriquecimineto.infraestructura.dto import ImagenAnonimizadaDTO, MetadatosImagenDTO
from saludtech.enriquecimiento.modulos.enriquecimineto.aplicacion.dto import ProcesarImagenDTO
from saludtech.enriquecimiento.modulos.enriquecimineto.aplicacion.servicios import ServicioAnonimizacion
from saludtech.enriquecimiento.seedwork.infraestructura import utils
from saludtech.enriquecimiento.modulos.enriquecimineto.infraestructura.schema.v1.eventos import EventoAnonimizacionIniciada, EventoAnonimizacionFinalizada
from saludtech.enriquecimiento.modulos.enriquecimineto.infraestructura.schema.v1.comandos import ComandoIniciarAnonimizacion
from saludtech.enriquecimiento.modulos.enriquecimineto.aplicacion.comandos.iniciar_anonimizacion import IniciarAnonimizacion
from saludtech.enriquecimiento.modulos.enriquecimineto.infraestructura.despachadores import Despachador
from saludtech.enriquecimiento.seedwork.aplicacion.comandos import ejecutar_commando
from saludtech.enriquecimiento.modulos.enriquecimineto.infraestructura.schema.v1.eventos import ReferenciaAlmacenamientoPayload

def suscribirse_a_eventos():
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('eventos-enriquecer', 'enriquecimiento-sub-eventos', consumer_type=_pulsar.ConsumerType.Shared, schema=AvroSchema(EventoAnonimizacionFinalizada))

        while True:
            mensaje = consumidor.receive()
            evento_integracion = mensaje.value().data
            print(f'---> Evento recibido: {evento_integracion}')

            id = evento_integracion.id
            imagen_anonimizada = db.session.query(ImagenAnonimizadaDTO).filter_by(id=id).first()

            print(f'---> Buscando entidad con ID: {str(id)} o la siguiente {id}')

            if imagen_anonimizada:
                if not imagen_anonimizada.metadatos:
                    nuevos_metadatos = MetadatosImagenDTO(
                        modalidad= random.choice(list(ModalidadImagen)),
                        region= random.choice(list(RegionAnatomica)),
                        resolucion = f'{{"ancho": {random.randint(60, 80)}, "alto": {random.randint(40, 60)}, "dpi": {random.randint(90, 110)}}}',
                        fecha_adquisicion=str(datetime.datetime.now())
                    )
                    db.session.add(nuevos_metadatos)
                    db.session.flush()

                    # Establecer la relación
                    imagen_anonimizada.metadatos_id = nuevos_metadatos.id
                    imagen_anonimizada.metadatos = nuevos_metadatos

                # Agregar más metadatos a la entidad existente
                imagen_anonimizada.estado = EstadoProceso.EXITOSO
                imagen_anonimizada.metadatos.modalidad = random.choice(list(ModalidadImagen))
                imagen_anonimizada.metadatos.region = random.choice(list(RegionAnatomica))
                imagen_anonimizada.metadatos.resolucion = f'{{"ancho": {random.randint(60, 80)}, "alto": {random.randint(40, 60)}, "dpi": {random.randint(90, 110)}}}'
                imagen_anonimizada.metadatos.fecha_adquisicion = str(datetime.datetime.now())

                db.session.commit()
                print(f'---> Metadatos actualizados para la entidad con ID: {id}')
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
                id = comando_integracion.id,
                referencia_salida = ReferenciaAlmacenamientoPayload(),
                timestamp = int(datetime.datetime.now().timestamp())
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