from saludtech.enriquecimiento.seedwork.aplicacion.servicios import Servicio
from saludtech.enriquecimiento.modulos.enriquecimineto.dominio.entidades import ImagenAnonimizada
from saludtech.enriquecimiento.modulos.enriquecimineto.dominio.fabricas import FabricaAnonimizacion
from saludtech.enriquecimiento.modulos.enriquecimineto.infraestructura.fabricas import FabricaRepositorio
from saludtech.enriquecimiento.modulos.enriquecimineto.infraestructura.repositorios import RepositorioImagenesAnonimizadas
from saludtech.enriquecimiento.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from .mapeadores import MapeadorImagenAnonimizada
from .dto import MetadatosImagenDTO, EstadoProcesoDTO, ProcesarImagenDTO, AjusteContrasteDTO, ResultadoProcesamientoDTO, ReferenciaAlmacenamientoDTO, ConfiguracionAnonimizacionDTO

import asyncio

class ServicioAnonimizacion(Servicio):

    def __init__(self):
        self._fabrica_repositorio: FabricaRepositorio = FabricaRepositorio()
        self._fabrica_anonimizacion: FabricaAnonimizacion = FabricaAnonimizacion()


    @property
    def fabrica_repositorio(self):
        return self._fabrica_repositorio
    
    @property
    def fabrica_anonimizacion(self):
        return self._fabrica_anonimizacion       
    
    def iniciar_anonimizacion(self, imagen_dto: ProcesarImagenDTO) -> ProcesarImagenDTO:
        imagen: ImagenAnonimizada = self.fabrica_anonimizacion.crear_objeto(imagen_dto, MapeadorImagenAnonimizada())
        imagen.iniciar_procesamiento(imagen)


        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioImagenesAnonimizadas.__class__)

        repositorio.agregar(imagen)
        UnidadTrabajoPuerto.registrar_batch(repositorio.agregar, imagen)
        UnidadTrabajoPuerto.savepoint()
        UnidadTrabajoPuerto.commit()

        return self.fabrica_anonimizacion.crear_objeto(imagen, MapeadorImagenAnonimizada())

    def obtener_reserva_por_id(self, id) -> ImagenAnonimizada:
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioImagenesAnonimizadas.__class__)
        return self.fabrica_anonimizacion.crear_objeto(repositorio.obtener_por_id(id), MapeadorImagenAnonimizada())

