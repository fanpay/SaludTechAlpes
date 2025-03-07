""" Repositorios para el manejo de persistencia de objetos de dominio en la capa de infrastructura del dominio de anonimizacion

En este archivo usted encontrará los diferentes repositorios para
persistir objetos dominio (agregaciones) en la capa de infraestructura del dominio de anonimizacion

"""

import json
import uuid
from saludtech.transformaciones.config.db import db
from saludtech.transformaciones.modulos.anonimizacion.dominio.repositorios import RepositorioImagenesAnonimizadas, RepositorioProcesosAnonimizacion
from saludtech.transformaciones.modulos.anonimizacion.dominio.entidades import ImagenAnonimizada
from saludtech.transformaciones.modulos.anonimizacion.infraestructura.dto import ImagenAnonimizadaDTO
from saludtech.transformaciones.modulos.anonimizacion.infraestructura.mapeadores import MapeadorImagenAnonimizada, MapeadorRespuestaImagenAnonimizada
from saludtech.transformaciones.modulos.anonimizacion.dominio.fabricas import FabricaAnonimizacion
from sqlalchemy.exc import NoResultFound
from uuid import UUID
from .dto import Saga_Log


class RepositorioImagenesAnonimizadasDB(RepositorioImagenesAnonimizadas):
    def __init__(self):
        self._fabrica_anonimizacion: FabricaAnonimizacion = FabricaAnonimizacion()

    @property
    def fabrica_anonimizacion(self):
        return self._fabrica_anonimizacion 
    
    def obtener_por_id(self, id: UUID) -> ImagenAnonimizada:
        imagen_dto = db.session.query(ImagenAnonimizadaDTO).filter_by(id=str(id)).one()
        return self.fabrica_anonimizacion.crear_objeto(imagen_dto, MapeadorRespuestaImagenAnonimizada())


    def obtener_todos(self) -> list[ImagenAnonimizada]:
        imagenes_dto = db.session.query(ImagenAnonimizadaDTO).all()
        mapeador = MapeadorImagenAnonimizada()
        return [mapeador.dto_a_entidad(imagen_dto) for imagen_dto in imagenes_dto]

    def agregar(self, imagen: ImagenAnonimizada):
        imagen_dto = self.fabrica_anonimizacion.crear_objeto(imagen, MapeadorImagenAnonimizada())
        db.session.add(imagen_dto)
        db.session.commit()
        print("Imagen anonimizada ID: " + str(imagen_dto.id))
        print("Metadatos anonimizados ID: " + str(imagen_dto.metadatos.id))
        print("Configuracion anonimizada guardada ID: " + str(imagen_dto.configuracion.id))
        print("Referencia_entrada anonimizada guardada ID: " + str(imagen_dto.referencia_entrada.id))

    def actualizar(self, imagen: ImagenAnonimizada):
        try:
            imagen_dto = db.session.query(ImagenAnonimizadaDTO).filter_by(id=str(imagen.id)).one_or_none()
            if imagen_dto:
                for key, value in MapeadorImagenAnonimizada().entidad_a_dto(imagen).__dict__.items():
                    #if key != '_sa_instance_state':
                    setattr(imagen_dto, key, value)
            else:
                db.session.add(MapeadorImagenAnonimizada().entidad_a_dto(imagen))
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def eliminar(self, id: UUID):
        try:
            imagen_dto = db.session.query(ImagenAnonimizadaDTO).filter_by(id=str(id)).one()
            db.session.delete(imagen_dto)
            db.session.commit()
        except NoResultFound:
            return False
        except Exception as e:
            db.session.rollback()
            raise e

class RepositorioProcesosAnonimizacionDB(RepositorioProcesosAnonimizacion):
    # Implementación similar a RepositorioImagenesAnonimizadasDB
    ...
    
    
class RepositorioSagaLogPostgresSQL():         

    def agregar(self, id_correlacion: str, evento: str, estado: str, datos: dict):
        # Serializar el payload si es necesario
        datos_serializados = json.dumps(datos) if isinstance(datos, dict) else datos
        
        entrada_log = Saga_Log(
            id=uuid.uuid4().hex,
            id_correlacion=id_correlacion,
            evento=evento,
            estado=estado,
            datos=datos_serializados
        )
        
        db.session.add(entrada_log)
        db.session.commit()

    def obtener_por_correlacion(self, id_correlacion: str) -> list[Saga_Log]:
        return db.session.query(Saga_Log)\
            .filter(Saga_Log.id_correlacion == id_correlacion)\
            .order_by(Saga_Log.fecha_evento.asc())\
            .all()