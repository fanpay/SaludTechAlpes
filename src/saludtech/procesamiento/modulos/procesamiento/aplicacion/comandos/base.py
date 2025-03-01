from saludtech.procesamiento.seedwork.aplicacion.comandos import ComandoHandler
from saludtech.procesamiento.modulos.procesamiento.infraestructura.fabricas import FabricaRepositorio
from saludtech.procesamiento.modulos.procesamiento.dominio.fabricas import FabricaAnonimizacion

class IniciarAnonimizacionBaseHandler(ComandoHandler):
    def __init__(self):
        self._fabrica_repositorio: FabricaRepositorio = FabricaRepositorio()
        self._fabrica_anonimizacion: FabricaAnonimizacion = FabricaAnonimizacion()

    @property
    def fabrica_repositorio(self):
        return self._fabrica_repositorio
    
    @property
    def fabrica_anonimizacion(self):
        return self._fabrica_anonimizacion      
    