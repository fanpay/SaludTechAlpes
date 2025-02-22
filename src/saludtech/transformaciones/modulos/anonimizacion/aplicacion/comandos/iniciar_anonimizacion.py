from datetime import datetime
from saludtech.transformaciones.modulos.anonimizacion.aplicacion.dto import AjusteContrasteDTO, ConfiguracionAnonimizacionDTO, ImagenAnonimizadaDTO, MetadatosImagenDTO, ProcesarImagenDTO, ReferenciaAlmacenamientoDTO
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
        procesar_dto = ProcesarImagenDTO(
                metadatos=MetadatosImagenDTO(
                modalidad=ModalidadImagen.RAYOS_X,
                region="TORAX",
                resolucion_ancho=2048,
                resolucion_alto=1024,
                fecha_adquisicion=datetime.now()
            ),
            configuracion=ConfiguracionAnonimizacionDTO(
                nivel_anonimizacion=3,
                formato_salida=FormatoSalida.DICOM,
                ajustes_contraste=AjusteContrasteDTO(brillo=1.2, contraste=0.8),
                algoritmo=AlgoritmoAnonimizacion.DICOM_DEID
            ),
            referencia_entrada=ReferenciaAlmacenamientoDTO(
                nombre_bucket="raw-images",
                llave_objeto="imagen_123.dcm",
                proveedor_almacenamiento="S3"
            )
        )
        
        # Convertir el DTO en una entidad de dominio
        imagen: ImagenAnonimizada = MapeadorImagenAnonimizada().dto_a_entidad(procesar_dto)

        # Ejecutar la lógica de anonimización en la entidad
        imagen.iniciar_procesamiento()

        # Obtener el repositorio de imágenes
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioImagenesAnonimizadas.__class__)

        UnidadTrabajoPuerto.registrar_batch(repositorio.agregar , imagen)
        UnidadTrabajoPuerto.savepoint()
        UnidadTrabajoPuerto.commit()


@comando.register(IniciarAnonimizacion)
def ejecutar_comando_procesar_imagen(comando: IniciarAnonimizacion):
    handler = IniciarAnonimizacionHandler()
    handler.handle(comando)