from saludtech.transformaciones.modulos.anonimizacion.aplicacion.coordinadores.saga_anonimizacion import CoordinadorSagaAnonimizacion
from saludtech.transformaciones.modulos.anonimizacion.dominio.eventos import (
    ProcesoAnonimizacionIniciado,
    ProcesoAnonimizacionFinalizado,
    ProcesoAnonimizacionFallido
)
from saludtech.transformaciones.modulos.anonimizacion.infraestructura.repositorios import RepositorioSagaLogPostgresSQL
from saludtech.transformaciones.seedwork.aplicacion.handlers import Handler
from saludtech.transformaciones.modulos.anonimizacion.infraestructura.despachadores import Despachador
from saludtech.transformaciones.seedwork.dominio.eventos import EventoDominio

class HandlerAnonimizacionIntegracion(Handler):

    @staticmethod
    def handle_proceso_anonimizacion_iniciado(evento: ProcesoAnonimizacionIniciado):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-anonimizacion')

    @staticmethod
    def handle_proceso_anonimizacion_finalizado(evento: ProcesoAnonimizacionFinalizado):
        print("Proceso de anonimizacion finalizado")
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-anonimizacion')

    @staticmethod
    def handle_proceso_anonimizacion_fallido(evento: ProcesoAnonimizacionFallido):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-anonimizacion')
        
        
class HandlerSagaAnonimizacion(Handler):

    def handle(self, evento: EventoDominio):
        if isinstance(evento, ProcesoAnonimizacionIniciado):
            coordinador = CoordinadorSagaAnonimizacion()
            coordinador.iniciar()
            
