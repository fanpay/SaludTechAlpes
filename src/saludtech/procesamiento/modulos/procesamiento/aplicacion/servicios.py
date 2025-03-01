from saludtech.procesamiento.seedwork.aplicacion.servicios import Servicio
from saludtech.procesamiento.modulos.procesamiento.dominio.entidades import Imagen
from saludtech.procesamiento.modulos.procesamiento.dominio.fabricas import FabricaAnonimizacion
from saludtech.procesamiento.modulos.procesamiento.infraestructura.fabricas import FabricaRepositorio
from saludtech.procesamiento.modulos.procesamiento.infraestructura.repositorios import RepositorioImagenes
from saludtech.procesamiento.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from .mapeadores import MapeadorImagen
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
        imagen: Imagen = self.fabrica_anonimizacion.crear_objeto(imagen_dto, MapeadorImagen())
        imagen.iniciar_procesamiento(imagen)


        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioImagenes.__class__)

        repositorio.agregar(imagen)
        UnidadTrabajoPuerto.registrar_batch(repositorio.agregar, imagen)
        UnidadTrabajoPuerto.savepoint()
        UnidadTrabajoPuerto.commit()

        return self.fabrica_anonimizacion.crear_objeto(imagen, MapeadorImagen())

    def obtener_reserva_por_id(self, id) -> Imagen:
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioImagenes.__class__)
        return self.fabrica_anonimizacion.crear_objeto(repositorio.obtener_por_id(id), MapeadorImagen())

