""" Mapeadores para la capa de infrastructura del dominio de anonimizacion

En este archivo usted encontrará los diferentes mapeadores
encargados de la transformación entre formatos de dominio y DTOs

"""

from saludtech.transformaciones.seedwork.dominio.repositorios import Mapeador
from saludtech.transformaciones.modulos.anonimizacion.dominio.entidades import ImagenAnonimizada
from saludtech.transformaciones.modulos.anonimizacion.dominio.objetos_valor import AlgoritmoAnonimizacion, EstadoProceso, FormatoSalida, MetadatosImagen, ConfiguracionAnonimizacion, ModalidadImagen, RegionAnatomica, ResultadoProcesamiento, ReferenciaAlmacenamiento
from saludtech.transformaciones.modulos.anonimizacion.infraestructura.dto import ImagenAnonimizadaDTO, MetadatosImagenDTO, ConfiguracionAnonimizacionDTO, ReferenciaAlmacenamientoDTO

class MapeadorImagenAnonimizada(Mapeador):

    def entidad_a_dto(self, entidad: ImagenAnonimizada) -> ImagenAnonimizadaDTO:
        return ImagenAnonimizadaDTO(
            id=str(entidad.id),
            estado=entidad.estado.value,
            resultado=entidad.resultado.checksum if entidad.resultado else None,
            fecha_solicitud=entidad.fecha_solicitud,
            metadatos_id=str(entidad.metadatos.id),
            configuracion_id=str(entidad.configuracion.id),
            referencia_entrada_id=str(entidad.referencia_entrada.id),
            referencia_salida_id=str(entidad.referencia_salida.id) if entidad.referencia_salida else None
        )

    def dto_a_entidad(self, dto: ImagenAnonimizadaDTO) -> ImagenAnonimizada:
        return ImagenAnonimizada(
            id=dto.id,
            estado=EstadoProceso(dto.estado),
            resultado=ResultadoProcesamiento(
                checksum=dto.resultado,
                tamano_archivo=0,  # Asignar el tamaño del archivo si está disponible
                timestamp=dto.fecha_solicitud
            ) if dto.resultado else None,
            fecha_solicitud=dto.fecha_solicitud,
            metadatos=MetadatosImagen(
                id=dto.metadatos_id,
                modalidad=ModalidadImagen(dto.modalidad),
                region=RegionAnatomica(dto.region),
                resolucion=dto.resolucion,
                fecha_adquisicion=dto.fecha_adquisicion
            ),
            configuracion=ConfiguracionAnonimizacion(
                id=dto.configuracion_id,
                nivel_anonimizacion=dto.nivel_anonimizacion,
                formato_salida=FormatoSalida(dto.formato_salida),
                ajustes_contraste=dto.ajustes_contraste,
                algoritmo=AlgoritmoAnonimizacion(dto.algoritmo)
            ),
            referencia_entrada=ReferenciaAlmacenamiento(
                id=dto.referencia_entrada_id,
                nombre_bucket=dto.nombre_bucket,
                llave_objeto=dto.llave_objeto,
                proveedor_almacenamiento=dto.proveedor_almacenamiento
            ),
            referencia_salida=ReferenciaAlmacenamiento(
                id=dto.referencia_salida_id,
                nombre_bucket=dto.nombre_bucket,
                llave_objeto=dto.llave_objeto,
                proveedor_almacenamiento=dto.proveedor_almacenamiento
            ) if dto.referencia_salida_id else None
        )