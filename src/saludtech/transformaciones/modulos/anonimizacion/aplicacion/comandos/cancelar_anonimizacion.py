from saludtech.transformaciones.seedwork.aplicacion.comandos import Comando, ComandoHandler, ejecutar_commando as comando

from dataclasses import dataclass, field
@dataclass
class CancelarAnonimizacion(Comando):
    id: str
    motivo: str

class CancelarAnonimizacionHandler(ComandoHandler):
    def handle(self, comando: CancelarAnonimizacion):
        print(f"Cancelando anonimizacion con id: {comando.id} y motivo: {comando.motivo}")
        
    
    
@comando.register(CancelarAnonimizacion)
def ejecutar_comando_cancelar_imagen(comando: CancelarAnonimizacion):
    handler = CancelarAnonimizacionHandler()
    handler.handle(comando)
    
