from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UsuarioBase(BaseModel):
    nombre: str
    correo: EmailStr 
    rol: str
    activo: bool = True

class UsuarioCreate(UsuarioBase):
    password: str 

class UsuarioOut(UsuarioBase):
    id_usuario: int

    class Config:
        from_attributes = True

class LaboratorioBase(BaseModel):
    nombre: str
    ubicacion: str
    activo: bool = True

class LaboratorioCreate(LaboratorioBase):
    pass

class LaboratorioOut(LaboratorioBase):
    id_laboratorio: int

    class Config:
        from_attributes = True

class ServicioBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    activo: bool = True

class ServicioCreate(ServicioBase):
    pass

class ServicioOut(ServicioBase):
    id_servicio: int

    class Config:
        from_attributes = True

class TicketBase(BaseModel):
    id_laboratorio: int
    id_servicio: int
    titulo: str
    descripcion: str
    prioridad: str

class TicketCreate(TicketBase):
    id_solicitante: int 

class TicketUpdateEstado(BaseModel):
    estado: str
    observacion_responsable: Optional[str] = None
    observacion_tecnico: Optional[str] = None

class TicketOut(TicketBase):
    id_ticket: int
    id_solicitante: int
    id_responsable: Optional[int] = None
    id_asignado: Optional[int] = None
    estado: str
    observacion_responsable: Optional[str] = None
    observacion_tecnico: Optional[str] = None
    fecha_creacion: datetime
    fecha_actualizacion: datetime
    fecha_finalizacion: Optional[datetime] = None

    class Config:
        from_attributes = True