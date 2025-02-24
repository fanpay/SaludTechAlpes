""" Mapeadores para la capa de infrastructura del dominio de anonimizacion

En este archivo usted encontrará los diferentes mapeadores
encargados de la transformación entre formatos de dominio y DTOs

"""

from saludtech.transformaciones.seedwork.dominio.objetos_valor import Resolucion
from saludtech.transformaciones.seedwork.dominio.repositorios import Mapeador
from saludtech.transformaciones.modulos.anonimizacion.dominio.entidades import ImagenAnonimizada
from saludtech.transformaciones.modulos.anonimizacion.dominio.objetos_valor import AlgoritmoAnonimizacion, EstadoProceso, FormatoSalida, MetadatosImagen, ConfiguracionAnonimizacion, ModalidadImagen, RegionAnatomica, ResultadoProcesamiento, ReferenciaAlmacenamiento
from saludtech.transformaciones.modulos.anonimizacion.infraestructura.dto import ImagenAnonimizadaDTO, MetadatosImagenDTO, ConfiguracionAnonimizacionDTO, ReferenciaAlmacenamientoDTO
import json

class MapeadorImagenAnonimizada(Mapeador):
    def obtener_tipo(self) -> type:
        return ImagenAnonimizada.__class__

    def entidad_a_dto(self, entidad: ImagenAnonimizada) -> ImagenAnonimizadaDTO:
        return ImagenAnonimizadaDTO(
            id=str(entidad.id),
            estado=entidad.estado.value,
            #resultado=entidad.resultado.checksum if entidad.resultado else None,
            fecha_solicitud=entidad.fecha_solicitud,
            metadatos=MetadatosImagenDTO(
                modalidad=entidad.metadatos.modalidad,
                region=entidad.metadatos.region,
                resolucion=json.dumps({
                    'ancho': entidad.metadatos.resolucion.ancho,
                    'alto': entidad.metadatos.resolucion.alto,
                    'dpi': entidad.metadatos.resolucion.dpi
                }),
                fecha_adquisicion=entidad.metadatos.fecha_adquisicion
            ),
            configuracion=ConfiguracionAnonimizacionDTO(
                nivel_anonimizacion=entidad.configuracion.nivel_anonimizacion,
                formato_salida=entidad.configuracion.formato_salida,
                ajustes_contraste=json.dumps({
                    'brillo': entidad.configuracion.ajustes_contraste.brillo,
                    'contraste': entidad.configuracion.ajustes_contraste.contraste
                }),
                algoritmo=entidad.configuracion.algoritmo
            ),
            referencia_entrada=ReferenciaAlmacenamientoDTO(
                nombre_bucket = entidad.referencia_entrada.nombre_bucket,
                llave_objeto = entidad.referencia_entrada.llave_objeto,
                proveedor_almacenamiento = entidad.referencia_entrada.proveedor_almacenamiento
            )
            #referencia_salida_id=str(entidad.referencia_salida.id) if entidad.referencia_salida else None
        )

    def dto_a_entidad(self, dto: ImagenAnonimizadaDTO) -> ImagenAnonimizada:
        resolucion_data = json.loads(dto.metadatos.resolucion)
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
                #id=dto.metadatos_id,
                modalidad=ModalidadImagen(dto.modalidad),
                region=RegionAnatomica(dto.region),
                resolucion=Resolucion(
                    ancho=dto.metadatos.resolucion['ancho'],
                    alto=resolucion_data['alto'],
                    dpi=resolucion_data['dpi']
                ),
                fecha_adquisicion=dto.fecha_adquisicion
            ),
            configuracion=ConfiguracionAnonimizacion(
                #id=dto.configuracion_id,
                nivel_anonimizacion=dto.nivel_anonimizacion,
                formato_salida=FormatoSalida(dto.formato_salida),
                ajustes_contraste=dto.ajustes_contraste,
                algoritmo=AlgoritmoAnonimizacion(dto.algoritmo)
            ),
            referencia_entrada=ReferenciaAlmacenamiento(
                #id=dto.referencia_entrada_id,
                nombre_bucket=dto.nombre_bucket,
                llave_objeto=dto.llave_objeto,
                proveedor_almacenamiento=dto.proveedor_almacenamiento
            ),
            referencia_salida=ReferenciaAlmacenamiento(
                #id=dto.referencia_salida_id,
                nombre_bucket=dto.nombre_bucket,
                llave_objeto=dto.llave_objeto,
                proveedor_almacenamiento=dto.proveedor_almacenamiento
            ) if dto.referencia_salida_id else None
        )
        
class MapeadorRespuestaImagenAnonimizada(Mapeador):
    def obtener_tipo(self) -> type:
        return ImagenAnonimizada.__class__
    
    def entidad_a_dto(self, entidad: ImagenAnonimizada) -> ImagenAnonimizadaDTO:
        return ImagenAnonimizadaDTO(
            id=str(entidad.id),
            estado=entidad.estado.value
        )

    def dto_a_entidad(self, dto: ImagenAnonimizadaDTO) -> ImagenAnonimizada:
        return ImagenAnonimizada(
            id=dto.id,
            estado=EstadoProceso(dto.estado),
            metadatos=dto.metadatos,
            configuracion=dto.configuracion,
            referencia_entrada=dto.referencia_entrada
        )