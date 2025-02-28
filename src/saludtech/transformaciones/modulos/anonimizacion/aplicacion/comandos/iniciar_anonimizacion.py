from datetime import datetime
from saludtech.transformaciones.modulos.anonimizacion.aplicacion.dto import AjusteContrasteDTO, ConfiguracionAnonimizacionDTO, EstadoProcesoDTO, ResultadoProcesamientoDTO, MetadatosImagenDTO, ProcesarImagenDTO, ReferenciaAlmacenamientoDTO
from saludtech.transformaciones.modulos.anonimizacion.aplicacion.mapeadores import MapeadorImagenAnonimizada
from saludtech.transformaciones.modulos.anonimizacion.dominio.entidades import ImagenAnonimizada
from saludtech.transformaciones.modulos.anonimizacion.dominio.objetos_valor import AlgoritmoAnonimizacion, FormatoSalida, ModalidadImagen
from saludtech.transformaciones.seedwork.aplicacion.comandos import Comando

from .base import IniciarAnonimizacionBaseHandler
from dataclasses import dataclass, field
from saludtech.transformaciones.seedwork.aplicacion.comandos import ejecutar_commando as comando

from saludtech.transformaciones.modulos.anonimizacion.dominio.entidades import ImagenAnonimizada
from saludtech.transformaciones.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from saludtech.transformaciones.modulos.anonimizacion.aplicacion.mapeadores import MapeadorImagenAnonimizada
from saludtech.transformaciones.modulos.anonimizacion.infraestructura.repositorios import RepositorioImagenesAnonimizadas

@dataclass
class IniciarAnonimizacion(Comando):
    id: str
    metadatos: MetadatosImagenDTO
    configuracion: ConfiguracionAnonimizacionDTO
    referencia_entrada: ReferenciaAlmacenamientoDTO
    


class IniciarAnonimizacionHandler(IniciarAnonimizacionBaseHandler):
    
    def handle(self, comando: IniciarAnonimizacion):
        procesar_imagen_dto = ProcesarImagenDTO(
            id=comando.id,
            metadatos=comando.metadatos,
            configuracion=comando.configuracion,
            referencia_entrada=comando.referencia_entrada
        )
        
        # Convertir el DTO en una entidad de dominio
        imagen: ImagenAnonimizada = self.fabrica_anonimizacion.crear_objeto(procesar_imagen_dto, MapeadorImagenAnonimizada())
        # Ejecutar la lógica de anonimización en la entidad
        imagen.iniciar_procesamiento(imagen)

        # Obtener el repositorio de imágenes
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioImagenesAnonimizadas.__class__)

        UnidadTrabajoPuerto.registrar_batch(repositorio.agregar , imagen)
        UnidadTrabajoPuerto.savepoint()
        UnidadTrabajoPuerto.commit()


@comando.register(IniciarAnonimizacion)
def ejecutar_comando_procesar_imagen(comando: IniciarAnonimizacion):
    handler = IniciarAnonimizacionHandler()
    handler.handle(comando)