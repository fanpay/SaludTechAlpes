from saludtech.transformaciones.modulos.anonimizacion.aplicacion.dto import ConfiguracionAnonimizacionDTO, ImagenAnonimizadaDTO, MetadatosImagenDTO, ReferenciaAlmacenamientoDTO
from saludtech.transformaciones.modulos.anonimizacion.aplicacion.mapeadores import MapeadorImagenAnonimizada
from saludtech.transformaciones.modulos.anonimizacion.dominio.entidades import ImagenAnonimizada
from saludtech.transformaciones.seedwork.aplicacion.comandos import Comando
from saludtech.transformaciones.modulos.vuelos.aplicacion.dto import ItinerarioDTO, ReservaDTO
from .base import IniciarAnonimizacionBaseHandler
from dataclasses import dataclass, field
from saludtech.transformaciones.seedwork.aplicacion.comandos import ejecutar_commando as comando

from saludtech.transformaciones.modulos.vuelos.dominio.entidades import Reserva
from saludtech.transformaciones.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from saludtech.transformaciones.modulos.vuelos.aplicacion.mapeadores import MapeadorReserva
from saludtech.transformaciones.modulos.vuelos.infraestructura.repositorios import RepositorioReservas

@dataclass
class IniciarAnonimizacion(Comando):
    id: str
    metadatos: MetadatosImagenDTO
    configuracion: ConfiguracionAnonimizacionDTO
    referencia_entrada: ReferenciaAlmacenamientoDTO
    


class IniciarAnonimizacionHandler(IniciarAnonimizacionBaseHandler):
    
    def handle(self, comando: IniciarAnonimizacion):
        imagen_dto = ImagenAnonimizadaDTO(
            id=comando.id,
            metadatos=comando.metadatos,
            configuracion=comando.configuracion,
            referencia_entrada=comando.referencia_entrada,
            referencia_salida=None,  # Aún no hay salida
            estado="pendiente",
            resultado="",
            fecha_solicitud=str(datetime.now())
        )
        
        # Convertir el DTO en una entidad de dominio
        imagen: ImagenAnonimizada = MapeadorImagenAnonimizada().dto_a_entidad(imagen_dto)

        # Ejecutar la lógica de anonimización en la entidad
        imagen.iniciar_anonimizacion()

        # Obtener el repositorio de imágenes
        repositorio = RepositorioImagenes()

        reserva: Reserva = self.fabrica_vuelos.crear_objeto(reserva_dto, MapeadorReserva())
        reserva.crear_reserva(reserva)

        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioReservas.__class__)

        UnidadTrabajoPuerto.registrar_batch(repositorio.agregar, reserva)
        UnidadTrabajoPuerto.savepoint()
        UnidadTrabajoPuerto.commit()


@comando.register(CrearReserva)
def ejecutar_comando_crear_reserva(comando: CrearReserva):
    handler = CrearReservaHandler()
    handler.handle(comando)
    