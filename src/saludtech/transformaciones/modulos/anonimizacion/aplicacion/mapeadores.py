import uuid
from saludtech.transformaciones.modulos.anonimizacion.infraestructura.dto import ImagenAnonimizadaDTO
from saludtech.transformaciones.seedwork.aplicacion.dto import Mapeador as AppMap
from saludtech.transformaciones.seedwork.dominio.objetos_valor import Resolucion
from saludtech.transformaciones.seedwork.dominio.repositorios import Mapeador as RepMap
from saludtech.transformaciones.modulos.anonimizacion.dominio.entidades import ImagenAnonimizada
from saludtech.transformaciones.modulos.anonimizacion.dominio.objetos_valor import AlgoritmoAnonimizacion, EstadoProceso, FormatoSalida, MetadatosImagen, ConfiguracionAnonimizacion, ModalidadImagen, RegionAnatomica, ResultadoProcesamiento, ReferenciaAlmacenamiento
from .dto import AjusteContrasteDTO, EstadoProcesoDTO, MetadatosImagenDTO, ConfiguracionAnonimizacionDTO, ProcesarImagenDTO, ResolucionDTO, ResultadoProcesamientoDTO, ReferenciaAlmacenamientoDTO

class MapeadorImagenAnonimizadaDTOJson(AppMap):
    def _procesar_metadatos(self, metadatos: dict) -> MetadatosImagenDTO:
        
        return MetadatosImagenDTO(
            modalidad=metadatos.get('modalidad'),
            region=metadatos.get('region'),
            resolucion=ResolucionDTO(
                ancho = metadatos.get('resolucion')['ancho'],
                alto = metadatos.get('resolucion')['alto'],
                dpi = metadatos.get('resolucion')['dpi']
            ),
            fecha_adquisicion=metadatos.get('fecha_adquisicion')
        )

    def _procesar_configuracion(self, configuracion: dict) -> ConfiguracionAnonimizacionDTO:
        return ConfiguracionAnonimizacionDTO(
            nivel_anonimizacion=configuracion.get('nivel_anonimizacion'),
            formato_salida=configuracion.get('formato_salida'),
            ajustes_contraste=AjusteContrasteDTO(
                brillo = configuracion.get('ajustes_contraste')['brillo'],
                contraste = configuracion.get('ajustes_contraste')['contraste']
            ),
            algoritmo_usado=configuracion.get('algoritmo')
        )

    def _procesar_resultado(self, resultado: dict) -> ResultadoProcesamientoDTO:
        return ResultadoProcesamientoDTO(
            checksum=resultado.get('checksum'),
            tamano_archivo=resultado.get('tamano_archivo'),
            timestamp=resultado.get('timestamp')
        )

    def _procesar_referencia(self, referencia: dict) -> ReferenciaAlmacenamientoDTO:
        return ReferenciaAlmacenamientoDTO(
            nombre_bucket=referencia.get('nombre_bucket'),
            llave_objeto=referencia.get('llave_objeto'),
            proveedor_almacenamiento=referencia.get('proveedor_almacenamiento')
        )

    def externo_a_dto(self, externo: dict) -> ProcesarImagenDTO:
        return ProcesarImagenDTO(
            metadatos=self._procesar_metadatos(externo.get('metadatos')),
            configuracion=self._procesar_configuracion(externo.get('configuracion')),
            referencia_entrada=self._procesar_referencia(externo.get('referencia_entrada'))
        )

    def dto_a_externo(self, dto: ProcesarImagenDTO) -> dict:
        return dto.__dict__

class MapeadorImagenAnonimizada(RepMap):
    def obtener_tipo(self) -> type:
        return ImagenAnonimizada.__class__
    
    def entidad_a_dto(self, entidad: ImagenAnonimizada) -> ImagenAnonimizadaDTO:
        return ImagenAnonimizadaDTO(
            id=str(entidad.id),
            metadatos=MetadatosImagenDTO(
                modalidad=entidad.metadatos.modalidad.value,
                region=entidad.metadatos.region.value,
                resolucion=entidad.metadatos.resolucion.value,
                fecha_adquisicion=entidad.metadatos.fecha_adquisicion
            ),
            configuracion=ConfiguracionAnonimizacionDTO(
                nivel_anonimizacion=entidad.configuracion.nivel_anonimizacion,
                formato_salida=entidad.configuracion.formato_salida.value,
                ajustes_contraste=entidad.configuracion.ajustes_contraste,
                algoritmo=entidad.configuracion.algoritmo.value
            ),
            referencia_entrada=ReferenciaAlmacenamientoDTO(
                nombre_bucket=entidad.referencia_entrada.nombre_bucket,
                llave_objeto=entidad.referencia_entrada.llave_objeto,
                proveedor_almacenamiento=entidad.referencia_entrada.proveedor_almacenamiento
            ),
            referencia_salida=ReferenciaAlmacenamientoDTO(
                nombre_bucket=entidad.referencia_salida.nombre_bucket,
                llave_objeto=entidad.referencia_salida.llave_objeto,
                proveedor_almacenamiento=entidad.referencia_salida.proveedor_almacenamiento
            ),
            estado=entidad.estado.value,
            resultado=ResultadoProcesamientoDTO(
                checksum=entidad.resultado.checksum,
                tamano_archivo=entidad.resultado.tamano_archivo,
                timestamp=entidad.resultado.timestamp
            ),
            fecha_solicitud=entidad.fecha_solicitud
        )

    def dto_a_entidad(self, dto: ImagenAnonimizadaDTO) -> ImagenAnonimizada:
        return ImagenAnonimizada(
            id=str(uuid.uuid4()),
            metadatos=MetadatosImagen(
                modalidad=ModalidadImagen(dto.metadatos.modalidad),
                region=RegionAnatomica(dto.metadatos.region),
                resolucion=Resolucion(
                    alto = dto.metadatos.resolucion.alto,
                    ancho = dto.metadatos.resolucion.ancho,
                    dpi = dto.metadatos.resolucion.dpi
                ),
                fecha_adquisicion=dto.metadatos.fecha_adquisicion
            ),
            configuracion=ConfiguracionAnonimizacion(
                nivel_anonimizacion=dto.configuracion.nivel_anonimizacion,
                formato_salida=FormatoSalida(dto.configuracion.formato_salida),
                ajustes_contraste=dto.configuracion.ajustes_contraste,
                algoritmo=AlgoritmoAnonimizacion(dto.configuracion.algoritmo)
            ),
            referencia_entrada=ReferenciaAlmacenamiento(
                nombre_bucket=dto.referencia_entrada.nombre_bucket,
                llave_objeto=dto.referencia_entrada.llave_objeto,
                proveedor_almacenamiento=dto.referencia_entrada.proveedor_almacenamiento
            )
            
        )
        
        
class MapeadorRespuestaImagenAnonimizadaDTOJson(AppMap):
    def externo_a_dto(self, externo: dict) -> ProcesarImagenDTO:
        return ProcesarImagenDTO(
            metadatos=self._procesar_metadatos(externo.get('metadatos')),
            configuracion=self._procesar_configuracion(externo.get('configuracion')),
            referencia_entrada=self._procesar_referencia(externo.get('referencia_entrada'))
        )

    def dto_a_externo(self, dto: EstadoProcesoDTO) -> dict:
        print("HOLA " + str(dto))
        return dto.__dict__
    

class MapeadorRespuestaImagenAnonimizada(RepMap):
    def obtener_tipo(self) -> type:
        return ImagenAnonimizada.__class__
    
    def entidad_a_dto(self, entidad: ImagenAnonimizada) -> EstadoProcesoDTO:
        return EstadoProcesoDTO(
            id=str(entidad.id),
            estado=entidad.estado,
            metadatos=MetadatosImagenDTO(
                modalidad=entidad.metadatos.modalidad,
                region=entidad.metadatos.region,
                resolucion=entidad.metadatos.resolucion,
                fecha_adquisicion=entidad.metadatos.fecha_adquisicion
            ),
            referencia_entrada=ReferenciaAlmacenamientoDTO(
                nombre_bucket=entidad.referencia_entrada.nombre_bucket,
                llave_objeto=entidad.referencia_entrada.llave_objeto,
                proveedor_almacenamiento=entidad.referencia_entrada.proveedor_almacenamiento
            ),
            referencia_salida=None,
            resultado=None,
            fecha_solicitud=entidad.fecha_solicitud,
            fecha_ultima_actualizacion=entidad.fecha_actualizacion,
            error=None
        )


    def dto_a_entidad(self, dto: EstadoProcesoDTO) -> ImagenAnonimizada:
        return ImagenAnonimizada(
            id=str(uuid.uuid4()),
            metadatos=None,
            configuracion=None,
            referencia_entrada=None,
            estado=dto.estado
        )