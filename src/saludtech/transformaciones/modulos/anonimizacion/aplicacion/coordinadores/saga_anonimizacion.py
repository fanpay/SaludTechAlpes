import uuid

from saludtech.transformaciones.modulos.anonimizacion.infraestructura.despachadores import Despachador
from saludtech.transformaciones.modulos.anonimizacion.infraestructura.schema.v1.eventos import EventoAnonimizacionFinalizada
from saludtech.transformaciones.seedwork.aplicacion.comandos import Comando
from saludtech.transformaciones.seedwork.aplicacion.sagas import CoordinadorOrquestacion, Paso, Transaccion, Inicio, Fin
from saludtech.transformaciones.seedwork.dominio.eventos import EventoDominio
from saludtech.transformaciones.modulos.anonimizacion.aplicacion.comandos import iniciar_anonimizacion, cancelar_anonimizacion
from saludtech.transformaciones.modulos.anonimizacion.dominio.eventos import ProcesoAnonimizacionFallido, ProcesoAnonimizacionFinalizado, ProcesoAnonimizacionIniciado
from saludtech.transformaciones.seedwork.infraestructura.schema.v1.eventos import EventoIntegracion

class CoordinadorSagaAnonimizacion(CoordinadorOrquestacion):
    def __init__(self):
        super().__init__()
        self.id_correlacion = str(uuid.uuid4())
        self.inicializar_pasos()
    
    def inicializar_pasos(self):
        self.pasos = [
            Inicio(index=0),
            Transaccion(
                index=1,
                comando=iniciar_anonimizacion.IniciarAnonimizacion,
                evento=ProcesoAnonimizacionIniciado,
                error=ProcesoAnonimizacionFallido,
                compensacion=cancelar_anonimizacion.CancelarAnonimizacion,
                exitosa=True
            ),
            Fin()
        ]

    def construir_comando(self, evento: EventoDominio, tipo_comando: type) -> Comando:
        # Mapear evento a comando específico
        if isinstance(evento, ProcesoAnonimizacionIniciado):
            return iniciar_anonimizacion.IniciarAnonimizacion(
                id=evento.proceso_id,
                metadatos=evento.metadatos,
                configuracion=evento.configuracion,
                referencia_entrada=evento.referencia_entrada
            )
        elif isinstance(evento, ProcesoAnonimizacionFallido):
            return cancelar_anonimizacion.CancelarAnonimizacion(
                id=evento.id,
                motivo="Prueba motivo"
            )
        else:
            raise NotImplementedError(f"No se puede construir el comando {tipo_comando} a partir del evento {evento}")

    def persistir_en_saga_log(self, mensaje):
        #self.repositorio.agregar(self)
        
        # Opcional: Registrar en logger de aplicación
        print(f"Saga {self.id_correlacion} persistido | Evento: {type(mensaje).__name__} | Mensaje: {mensaje}")
        #repositorio_saga.agregar(self)

    def procesar_evento(self, evento: EventoDominio):
        paso, index = self.obtener_paso_dado_un_evento(evento)
        if self.es_ultima_transaccion(index) and not isinstance(evento, paso.error):
            self.terminar()
        
        if isinstance(evento, paso.error):
            if index > 0 and self.pasos[index].compensacion:
                self.publicar_comando(evento, self.pasos[index].compensacion)
                self.persistir_en_saga_log(f"Compensación iniciada: {evento}")
        
        elif isinstance(evento, paso.evento):
            if index < len(self.pasos) - 1:
                #siguiente_paso = self.pasos[index + 1]
                self.publicar_comando(evento, paso.comando)
                self.persistir_en_saga_log(f"Proceso exitoso: {evento}")

    def iniciar(self):
        self.persistir_en_saga_log(f"Se inicia SAGA: {self.id_correlacion}")
        
    def terminar(self):
        self.persistir_en_saga_log(f"Se finaliza SAGA: {self.id_correlacion}")
        
        
def oir_mensaje(mensaje):
    if isinstance(mensaje, EventoDominio):
        coordinador = CoordinadorSagaAnonimizacion()
        coordinador.procesar_evento(mensaje)
    else:
        raise NotImplementedError("El mensaje no es evento de Dominio")


def publicar_evento_integracion(mensaje, topico):
    if isinstance(mensaje, EventoIntegracion):
        despachador = Despachador()
        despachador.publicar_evento(mensaje, topico)