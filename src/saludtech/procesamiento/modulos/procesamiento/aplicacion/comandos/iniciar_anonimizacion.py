from datetime import datetime
from saludtech.procesamiento.modulos.procesamiento.aplicacion.dto import AjusteContrasteDTO, ConfiguracionAnonimizacionDTO, EstadoProcesoDTO, ResultadoProcesamientoDTO, MetadatosImagenDTO, ProcesarImagenDTO, ReferenciaAlmacenamientoDTO
from saludtech.procesamiento.modulos.procesamiento.aplicacion.mapeadores import MapeadorImagen
from saludtech.procesamiento.modulos.procesamiento.dominio.entidades import Imagen
from saludtech.procesamiento.modulos.procesamiento.dominio.objetos_valor import AlgoritmoAnonimizacion, FormatoSalida, ModalidadImagen
from saludtech.procesamiento.seedwork.aplicacion.comandos import Comando

from .base import IniciarAnonimizacionBaseHandler
from dataclasses import dataclass, field
from saludtech.procesamiento.seedwork.aplicacion.comandos import ejecutar_commando as comando

from saludtech.procesamiento.modulos.procesamiento.dominio.entidades import Imagen
from saludtech.procesamiento.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from saludtech.procesamiento.modulos.procesamiento.aplicacion.mapeadores import MapeadorImagen
from saludtech.procesamiento.modulos.procesamiento.infraestructura.repositorios import RepositorioImagenes

@dataclass
class IniciarAnonimizacion(Comando):
    id: str
    id_solicitud: str
    nombre: str
    cedula: int
    usuario: str
    metadatos: MetadatosImagenDTO
    configuracion: ConfiguracionAnonimizacionDTO
    referencia_entrada: ReferenciaAlmacenamientoDTO
    


class IniciarAnonimizacionHandler(IniciarAnonimizacionBaseHandler):
    
    def handle(self, comando: IniciarAnonimizacion):
        procesar_imagen_dto = ProcesarImagenDTO(
            id=comando.id,
            cedula=comando.cedula,
            nombre=comando.nombre,
            usuario=comando.usuario,
            id_solicitud=comando.id_solicitud,
            metadatos=comando.metadatos,
            configuracion=comando.configuracion,
            referencia_entrada=comando.referencia_entrada
        )
        
        # Convertir el DTO en una entidad de dominio
        imagen: Imagen = self.fabrica_anonimizacion.crear_objeto(procesar_imagen_dto, MapeadorImagen())
        # Ejecutar la lógica de anonimización en la entidad
        imagen.iniciar_procesamiento(imagen)

        # Obtener el repositorio de imágenes
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioImagenes.__class__)

        UnidadTrabajoPuerto.registrar_batch(repositorio.agregar , imagen)
        UnidadTrabajoPuerto.savepoint()
        UnidadTrabajoPuerto.commit()


@comando.register(IniciarAnonimizacion)
def ejecutar_comando_procesar_imagen(comando: IniciarAnonimizacion):
    handler = IniciarAnonimizacionHandler()
    handler.handle(comando)