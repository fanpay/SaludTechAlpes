"""Reglas de negocio del dominio de cliente

En este archivo usted encontrará reglas de negocio del dominio de cliente

"""

from saludtech.transformaciones.seedwork.dominio.reglas import ReglaNegocio
from .objetos_valor import ConfiguracionAnonimizacion, EstadoProceso, FormatoSalida, MetadatosImagen, ReferenciaAlmacenamiento
from .entidades import ImagenAnonimizada


class ImagenDebeTenerReferencia(ReglaNegocio):
    """Regla para verificar que la imagen tiene una referencia válida en el bucket."""
    
    referencia: ReferenciaAlmacenamiento

    def __init__(self, referencia: ReferenciaAlmacenamiento, mensaje="La imagen debe tener una referencia de almacenamiento válida."):
        super().__init__(mensaje)
        self.referencia = referencia

    def es_valido(self) -> bool:
        return bool(self.referencia.nombre_bucket and self.referencia.llave_objeto)


class ImagenDebeSerProcesable(ReglaNegocio):
    """Regla que verifica que la imagen esté en un estado válido para procesamiento."""

    imagen: ImagenAnonimizada

    def __init__(self, imagen: ImagenAnonimizada, mensaje="La imagen no puede procesarse en su estado actual."):
        super().__init__(mensaje)
        self.imagen = imagen

    def es_valido(self) -> bool:
        return self.imagen.estado in {EstadoProceso.PENDIENTE, EstadoProceso.PROCESANDO}
    

class NivelAnonimizacionValido(ReglaNegocio):
    def __init__(self, config: ConfiguracionAnonimizacion, mensaje='Nivel de anonimización inválido (1-5)'):
        super().__init__(mensaje)
        self.config = config

    def es_valido(self) -> bool:
        return isinstance(self.config.nivel_anonimizacion, int) and 1 <= self.config.nivel_anonimizacion <= 5

class FormatoImagenSoportado(ReglaNegocio):
    formatos_salida_soportados = {FormatoSalida.DICOM, FormatoSalida.NIFTI, FormatoSalida.PNG, FormatoSalida.JPEG}

    def __init__(self, configuracion_anonimizacion: ConfiguracionAnonimizacion, mensaje='Formato de imagen no compatible en la configuración de anonimización'):
        super().__init__(mensaje)
        self.configuracion_anonimizacion = configuracion_anonimizacion

    def es_valido(self) -> bool:
        return self.configuracion_anonimizacion.formato_salida in self.formatos_salida_soportados

class TransicionEstadoValida(ReglaNegocio):
    def __init__(self, estado_actual: EstadoProceso, nuevo_estado: EstadoProceso, 
                mensaje='Transición de estado inválida'):
        super().__init__(mensaje)
        self.estado_actual = estado_actual
        self.nuevo_estado = nuevo_estado

    def es_valido(self) -> bool:
        transiciones_permitidas = {
            EstadoProceso.PENDIENTE: [EstadoProceso.PROCESANDO],
            EstadoProceso.PROCESANDO: [EstadoProceso.EXITOSO, EstadoProceso.FALLIDO],
            EstadoProceso.FALLIDO: [EstadoProceso.PENDIENTE]
        }
        return self.nuevo_estado in transiciones_permitidas.get(self.estado_actual, [])

    
