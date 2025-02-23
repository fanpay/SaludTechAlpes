from saludtech.transformaciones.seedwork.aplicacion.queries import Query, QueryHandler, QueryResultado
from saludtech.transformaciones.seedwork.aplicacion.queries import ejecutar_query as query
from saludtech.transformaciones.modulos.anonimizacion.infraestructura.repositorios import RepositorioImagenesAnonimizadas
from dataclasses import dataclass
from .base import ReservaQueryBaseHandler
from saludtech.transformaciones.modulos.anonimizacion.aplicacion.mapeadores import MapeadorImagenAnonimizada
import uuid

@dataclass
class ObtenerEstadoProceso(Query):
    id: str

class ObtenerEstadoProcesoHandler(ReservaQueryBaseHandler):

    def handle(self, query: ObtenerEstadoProceso) -> QueryResultado:
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioImagenesAnonimizadas.__class__)
        reserva =  self.fabrica_anonimizacion.crear_objeto(repositorio.obtener_por_id(query.id), MapeadorImagenAnonimizada())
        return QueryResultado(resultado=reserva)

@query.register(ObtenerEstadoProceso)
def ejecutar_query_obtener_estado_proceso(query: ObtenerEstadoProceso):
    handler = ObtenerEstadoProcesoHandler()
    return handler.handle(query)