from saludtech.enriquecimiento.seedwork.aplicacion.queries import Query, QueryHandler, QueryResultado
from saludtech.enriquecimiento.seedwork.aplicacion.queries import ejecutar_query as query
from saludtech.enriquecimiento.modulos.anonimizacion.infraestructura.repositorios import RepositorioImagenesAnonimizadas
from dataclasses import dataclass
from .base import AnonimizacionQueryBaseHandler
from saludtech.enriquecimiento.modulos.anonimizacion.aplicacion.mapeadores import MapeadorRespuestaImagenAnonimizada
import uuid

@dataclass
class ObtenerEstadoProceso(Query):
    id: str

class ObtenerEstadoProcesoHandler(AnonimizacionQueryBaseHandler):

    def handle(self, query: ObtenerEstadoProceso) -> QueryResultado:
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioImagenesAnonimizadas.__class__)
        resultado =  self.fabrica_anonimizacion.crear_objeto(repositorio.obtener_por_id(query.id), MapeadorRespuestaImagenAnonimizada())
        return QueryResultado(resultado=resultado)

@query.register(ObtenerEstadoProceso)
def ejecutar_query_obtener_estado_proceso(query: ObtenerEstadoProceso):
    handler = ObtenerEstadoProcesoHandler()
    return handler.handle(query)