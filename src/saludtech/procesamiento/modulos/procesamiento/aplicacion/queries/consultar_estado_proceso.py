from saludtech.procesamiento.seedwork.aplicacion.queries import Query, QueryHandler, QueryResultado
from saludtech.procesamiento.seedwork.aplicacion.queries import ejecutar_query as query
from saludtech.procesamiento.modulos.procesamiento.infraestructura.repositorios import RepositorioImagenes
from dataclasses import dataclass
from .base import AnonimizacionQueryBaseHandler
from saludtech.procesamiento.modulos.procesamiento.aplicacion.mapeadores import MapeadorRespuestaImagen
import uuid

@dataclass
class ObtenerEstadoProceso(Query):
    usuario: str

class ObtenerEstadoProcesoHandler(AnonimizacionQueryBaseHandler):

    def handle(self, query: ObtenerEstadoProceso) -> QueryResultado:
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioImagenes.__class__)
        respuesta = repositorio.obtener_todos_por_ususario(query.usuario)
        mapper = MapeadorRespuestaImagen()
        resultado = [mapper.entidad_a_dto(item) for item in respuesta]
        
        return QueryResultado(resultado=resultado)

@query.register(ObtenerEstadoProceso)
def ejecutar_query_obtener_estado_proceso(query: ObtenerEstadoProceso):
    handler = ObtenerEstadoProcesoHandler()
    return handler.handle(query)