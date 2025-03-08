import pulsar,_pulsar  
from pulsar.schema import *
import uuid
import time
import logging
import traceback
import datetime

from saludtech.transformaciones.modulos.anonimizacion.aplicacion.coordinadores.saga_anonimizacion import CoordinadorSagaAnonimizacion, oir_mensaje, publicar_evento_integracion
from saludtech.transformaciones.modulos.anonimizacion.dominio.eventos import ProcesoAnonimizacionFallido, ProcesoAnonimizacionIniciado
from saludtech.transformaciones.modulos.anonimizacion.dominio.objetos_valor import EstadoProceso
from saludtech.transformaciones.modulos.anonimizacion.infraestructura.repositorios import RepositorioSagaLogPostgresSQL
from saludtech.transformaciones.seedwork.infraestructura import utils
from saludtech.transformaciones.modulos.anonimizacion.infraestructura.schema.v1.eventos import ConfiguracionAnonimizacionPayload, EventoAnonimizacionIniciada, EventoAnonimizacionFinalizada, EventoAnonimizacionFinalizadaPayload, EventoAnonimizacionFallida, EventoAnonimizacionIniciadaPayload, MetadatosImagenPayload
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

            comando = IniciarAnonimizacion(
                id=evento_integracion.id,
                metadatos=evento_integracion.metadatos,
                configuracion=evento_integracion.configuracion,
                referencia_entrada=evento_integracion.referencia_entrada
            )

            despachador = Despachador()
            despachador.publicar_comando(comando, 'comandos-anonimizacion11')
            consumidor.acknowledge(mensaje)

        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de eventos!')
        traceback.print_exc()
        if cliente:
            cliente.close()

def suscribirse_a_comandos_old():
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('comandos-anonimizacion-old', consumer_type=_pulsar.ConsumerType.Shared, subscription_name='saludtech-sub-comandos', schema=AvroSchema(ComandoIniciarAnonimizacion))

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
            
            
def suscribirse_a_comandos():
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('comandos-anonimizacion11', consumer_type=_pulsar.ConsumerType.Shared, 
                                     subscription_name='saludtech-sub-comandos', schema=AvroSchema(ComandoIniciarAnonimizacion))
        
    
        #repositorio_saga = RepositorioSagaLogPostgresSQL()

        while True:
            mensaje = consumidor.receive()
            comando_integracion = mensaje.value().data
            
            # 1. Iniciar Saga
            saga = CoordinadorSagaAnonimizacion()
            saga.iniciar()

            
            try:
                # 2. Crear evento de dominio
                evento_dominio_iniciado = ProcesoAnonimizacionIniciado(
                    proceso_id=comando_integracion.id,
                    metadatos=comando_integracion.metadatos,
                    configuracion=comando_integracion.configuracion,
                    referencia_entrada=comando_integracion.referencia_entrada
                )
                
                # 3. Procesar evento de dominio
                oir_mensaje(evento_dominio_iniciado)
                
                # 4. Publicar evento para Enriquecimiento
                evento_finalizado = EventoAnonimizacionFinalizada(
                    data = EventoAnonimizacionFinalizadaPayload(
                        id = comando_integracion.id,
                        referencia_salida = ReferenciaAlmacenamientoPayload(),
                        timestamp = int(datetime.datetime.now().timestamp())
                    )
                )
                
                publicar_evento_integracion(evento_finalizado, 'eventos-enriquecer')
                
                # 5. Actualizar estado (no completar aún, esperar confirmación)
                saga.persistir_en_saga_log(evento_finalizado)
                
                

            except Exception as e:
                # 6. Manejo de errores y compensación
                if saga:
                    evento_fallo = ProcesoAnonimizacionFallido(
                        id=saga.id_correlacion,
                        proceso_id=saga.id_correlacion,
                        motivo_fallo=str(e)
                    )
                    saga.procesar_evento(evento_fallo)
                    
                    #publicar_evento_integracion(evento_fallo, 'eventos-desenriquecer')
                    publicar_evento_integracion(evento_fallo, 'eventos-desprocesamiento')
                
                print(f"Error procesando comando: {str(e)}")
            finally:
                saga.terminar()
                consumidor.acknowledge(mensaje)
            
        cliente.close()
    except:
        logging.error('ERROR: Procesando comandos del saga!')
        traceback.print_exc()
        if cliente:
            cliente.close()