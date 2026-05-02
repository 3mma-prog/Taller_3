from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from typing import List
import models, schemas, crud
from db import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Mesa de Servicios Laboratorios",
    version = "0.1",
    description="API para gestión de tickets y servicios con JWT y Scopes"
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router_usuarios = APIRouter(prefix="/usuarios", tags=["Usuarios"])
router_laboratorios = APIRouter(prefix="/laboratorios", tags=["Laboratorios"])
router_servicios = APIRouter(prefix="/servicios", tags=["Servicios"])
router_tickets = APIRouter(prefix="/tickets", tags=["Tickets"])

@router_usuarios.post("/", response_model=schemas.UsuarioOut)
def create_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    db_user = crud.get_usuario_by_correo(db, correo=usuario.correo)
    if db_user:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")
    return crud.create_usuario(db, usuario)

@router_usuarios.get("/", response_model=List[schemas.UsuarioOut])
def read_usuarios(db: Session = Depends(get_db)):
    return crud.get_usuarios(db)

@router_usuarios.get("/{id_usuario}", response_model=schemas.UsuarioOut)
def read_usuario(id_usuario: int, db: Session = Depends(get_db)):
    usuario = crud.get_usuario_by_id(db, id_usuario)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@router_laboratorios.post("/", response_model=schemas.LaboratorioOut)
def create_laboratorio(laboratorio: schemas.LaboratorioCreate, db: Session = Depends(get_db)):
    return crud.create_laboratorio(db, laboratorio)

@router_laboratorios.get("/", response_model=List[schemas.LaboratorioOut])
def read_laboratorios(db: Session = Depends(get_db)):
    return crud.get_laboratorios(db)

@router_laboratorios.get("/{id_laboratorio}", response_model=schemas.LaboratorioOut)
def read_laboratorio(id_laboratorio: int, db: Session = Depends(get_db)):
    lab = crud.get_laboratorio_by_id(db, id_laboratorio)
    if not lab:
        raise HTTPException(status_code=404, detail="Laboratorio no encontrado")
    return lab

@router_servicios.post("/", response_model=schemas.ServicioOut)
def create_servicio(servicio: schemas.ServicioCreate, db: Session = Depends(get_db)):
    return crud.create_servicio(db, servicio)

@router_servicios.get("/", response_model=List[schemas.ServicioOut])
def read_servicios(db: Session = Depends(get_db)):
    return crud.get_servicios(db)

@router_servicios.get("/{id_servicio}", response_model=schemas.ServicioOut)
def read_servicio(id_servicio: int, db: Session = Depends(get_db)):
    servicio = crud.get_servicio_by_id(db, id_servicio)
    if not servicio:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    return servicio

@router_tickets.post("/", response_model=schemas.TicketOut)
def create_ticket(ticket: schemas.TicketCreate, db: Session = Depends(get_db)):
    return crud.create_ticket(db, ticket)

@router_tickets.get("/", response_model=List[schemas.TicketOut])
def read_tickets(db: Session = Depends(get_db)):
    return crud.get_tickets(db)

@router_tickets.get("/{id_ticket}", response_model=schemas.TicketOut)
def read_ticket(id_ticket: int, db: Session = Depends(get_db)):
    ticket = crud.get_ticket_by_id(db, id_ticket)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")
    return ticket

@router_tickets.patch("/{id_ticket}/estado", response_model=schemas.TicketOut)
def update_estado_ticket(id_ticket: int, datos: schemas.TicketUpdateEstado, db: Session = Depends(get_db)):
    ticket_actualizado = crud.update_ticket_estado(db, id_ticket, datos)
    if not ticket_actualizado:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")
    return ticket_actualizado

app.include_router(router_usuarios)
app.include_router(router_laboratorios)
app.include_router(router_servicios)
app.include_router(router_tickets)