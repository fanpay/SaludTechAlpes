from saludtech.procesamiento.modulos.procesamiento.dominio.eventos import (
    ProcesoAnonimizacionIniciado,
    ProcesoAnonimizacionFinalizado,
    ProcesoAnonimizacionFallido
)
from saludtech.procesamiento.seedwork.aplicacion.handlers import Handler
from saludtech.procesamiento.modulos.procesamiento.infraestructura.despachadores import Despachador

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