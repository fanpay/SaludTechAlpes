""" Repositorios para el manejo de persistencia de objetos de dominio en la capa de infrastructura del dominio de anonimizacion

En este archivo usted encontrará los diferentes repositorios para
persistir objetos dominio (agregaciones) en la capa de infraestructura del dominio de anonimizacion

"""

from saludtech.procesamiento.config.db import db
from saludtech.procesamiento.modulos.procesamiento.dominio.repositorios import RepositorioImagenes, RepositorioProcesosAnonimizacion
from saludtech.procesamiento.modulos.procesamiento.dominio.entidades import Imagen
from saludtech.procesamiento.modulos.procesamiento.infraestructura.dto import ImagenDTO
from saludtech.procesamiento.modulos.procesamiento.infraestructura.mapeadores import MapeadorImagen, MapeadorRespuestaImagen
from saludtech.procesamiento.modulos.procesamiento.dominio.fabricas import FabricaAnonimizacion
from sqlalchemy.exc import NoResultFound
from uuid import UUID

class RepositorioImagenesDB(RepositorioImagenes):
    def __init__(self):
        self._fabrica_anonimizacion: FabricaAnonimizacion = FabricaAnonimizacion()

    @property
    def fabrica_anonimizacion(self):
        return self._fabrica_anonimizacion 
    
    def obtener_por_id(self, id: UUID) -> Imagen:
        imagen_dto = db.session.query(ImagenDTO).filter_by(id=str(id)).one()
        return self.fabrica_anonimizacion.crear_objeto(imagen_dto, MapeadorRespuestaImagen())
    
    def obtener_todos_por_ususario(self, usuario: str) -> list[Imagen]:
        imagenes_dto = db.session.query(ImagenDTO).filter_by(usuario=str(usuario)).all()
        return [self.fabrica_anonimizacion.crear_objeto(imagen_dto, MapeadorRespuestaImagen()) for imagen_dto in imagenes_dto]


    def obtener_todos(self) -> list[Imagen]:
        imagenes_dto = db.session.query(ImagenDTO).all()
        mapeador = MapeadorImagen()
        return [mapeador.dto_a_entidad(imagen_dto) for imagen_dto in imagenes_dto]

    def agregar(self, imagen: Imagen):
        imagen_dto = self.fabrica_anonimizacion.crear_objeto(imagen, MapeadorImagen())
        db.session.add(imagen_dto)
        db.session.commit()
        print("Imagen  ID: " + str(imagen_dto.id))
        print("Metadatos anonimizados ID: " + str(imagen_dto.metadatos.id))
        print("Configuracion  guardada ID: " + str(imagen_dto.configuracion.id))
        print("Referencia_entrada  guardada ID: " + str(imagen_dto.referencia_entrada.id))

    def actualizar(self, imagen: Imagen):
        try:
            imagen_dto = db.session.query(ImagenDTO).filter_by(id=str(imagen.id)).one_or_none()
            if imagen_dto:
                for key, value in MapeadorImagen().entidad_a_dto(imagen).__dict__.items():
                    #if key != '_sa_instance_state':
                    setattr(imagen_dto, key, value)
            else:
                db.session.add(MapeadorImagen().entidad_a_dto(imagen))
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def eliminar(self, id: UUID):
        try:
            imagen_dto = db.session.query(ImagenDTO).filter_by(id=str(id)).one()
            db.session.delete(imagen_dto)
            db.session.commit()
        except NoResultFound:
            return False
        except Exception as e:
            db.session.rollback()
            raise e

class RepositorioProcesosAnonimizacionDB(RepositorioProcesosAnonimizacion):
    # Implementación similar a RepositorioImagenesDB
    ...