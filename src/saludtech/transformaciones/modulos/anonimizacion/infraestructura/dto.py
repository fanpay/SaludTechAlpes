"""DTOs para la capa de infraestructura del dominio de anonimización de imágenes

En este archivo se definen los DTOs (modelos anémicos) que serán utilizados
en la capa de persistencia para almacenar y recuperar entidades en la base de datos.
"""

from saludtech.transformaciones.config.db import db
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, String, Integer, DateTime
import uuid
from datetime import datetime

Base = db.declarative_base()

class ImagenAnonimizadaDTO(db.Model):
    """Modelo de tabla para almacenar imágenes anonimizadas."""
    __tablename__ = "imagenes_anonimizadas"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    estado = Column(String, nullable=False)
    resultado = Column(String, nullable=True)
    fecha_solicitud = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relaciones con otras tablas
    metadatos_id = Column(String, ForeignKey("metadatos_imagenes.id"), nullable=False)
    configuracion_id = Column(String, ForeignKey("configuraciones_anonimizacion.id"), nullable=False)
    referencia_entrada_id = Column(String, ForeignKey("referencias_almacenamiento.id"), nullable=False)
    referencia_salida_id = Column(String, ForeignKey("referencias_almacenamiento.id"), nullable=True)

    metadatos = relationship("MetadatosImagenDTO", backref="imagen_anonimizada")
    configuracion = relationship("ConfiguracionAnonimizacionDTO", backref="imagen_anonimizada")
    referencia_entrada = relationship("ReferenciaAlmacenamientoDTO", foreign_keys=[referencia_entrada_id])
    referencia_salida = relationship("ReferenciaAlmacenamientoDTO", foreign_keys=[referencia_salida_id])

class MetadatosImagenDTO(db.Model):
    """Modelo de tabla para almacenar metadatos de las imágenes."""
    __tablename__ = "metadatos_imagenes"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    modalidad = Column(String, nullable=False)
    region = Column(String, nullable=False)
    resolucion = Column(String, nullable=False)
    fecha_adquisicion = Column(DateTime, nullable=False)

class ConfiguracionAnonimizacionDTO(db.Model):
    """Modelo de tabla para almacenar configuraciones de anonimización."""
    __tablename__ = "configuraciones_anonimizacion"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    nivel_anonimizacion = Column(Integer, nullable=False)
    formato_salida = Column(String, nullable=False)
    ajustes_contraste = Column(String, nullable=True)  # Se almacena como JSON o string serializado
    algoritmo = Column(String, nullable=False)

class ReferenciaAlmacenamientoDTO(db.Model):
    """Modelo de tabla para almacenar referencias a objetos en almacenamiento."""
    __tablename__ = "referencias_almacenamiento"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    nombre_bucket = Column(String, nullable=False)
    llave_objeto = Column(String, nullable=False)
    proveedor_almacenamiento = Column(String, nullable=False)
