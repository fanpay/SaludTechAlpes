from saludtech.enriquecimiento.seedwork.aplicacion.queries import QueryHandler
from saludtech.enriquecimiento.modulos.anonimizacion.infraestructura.fabricas import FabricaRepositorio
from saludtech.enriquecimiento.modulos.anonimizacion.dominio.fabricas import FabricaAnonimizacion

class AnonimizacionQueryBaseHandler(QueryHandler):
    def __init__(self):
        self._fabrica_repositorio: FabricaRepositorio = FabricaRepositorio()
        self._fabrica_anonimizacion: FabricaAnonimizacion = FabricaAnonimizacion()

    @property
    def fabrica_repositorio(self):
        return self._fabrica_repositorio
    
    @property
    def fabrica_anonimizacion(self):
        return self._fabrica_anonimizacion    