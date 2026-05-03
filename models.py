from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from db import Base

mi_schema = "jwt_grupo_15" 

class Usuario(Base):
    __tablename__ = "usuarios"
    __table_args__ = {"schema": mi_schema}

    id_usuario = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    correo = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    rol = Column(String(50), nullable=False)
    activo = Column(Boolean, default=True)

class Laboratorio(Base):
    __tablename__ = "laboratorios"
    __table_args__ = {"schema": mi_schema}

    id_laboratorio = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    ubicacion = Column(String(100), nullable=False)
    activo = Column(Boolean, default=True)

class Servicio(Base):
    __tablename__ = "servicios"
    __table_args__ = {"schema": mi_schema}

    id_servicio = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String(255))
    activo = Column(Boolean, default=True)

class Ticket(Base):
    __tablename__ = "tickets"
    __table_args__ = {"schema": mi_schema}

    id_ticket = Column(Integer, primary_key=True, index=True)
    id_solicitante = Column(Integer, ForeignKey(f"{mi_schema}.usuarios.id_usuario"), nullable=False)
    id_laboratorio = Column(Integer, ForeignKey(f"{mi_schema}.laboratorios.id_laboratorio"), nullable=False)
    id_servicio = Column(Integer, ForeignKey(f"{mi_schema}.servicios.id_servicio"), nullable=False)
    id_responsable = Column(Integer, ForeignKey(f"{mi_schema}.usuarios.id_usuario"), nullable=True)
    id_asignado = Column(Integer, ForeignKey(f"{mi_schema}.usuarios.id_usuario"), nullable=True)
    titulo = Column(String(100), nullable=False)
    descripcion = Column(String(500), nullable=False)
    estado = Column(String(50), nullable=False, default="solicitado")
    prioridad = Column(String(50), nullable=False)
    observacion_responsable = Column(String(500), nullable=True)
    observacion_tecnico = Column(String(500), nullable=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_actualizacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    fecha_finalizacion = Column(DateTime, nullable=True)