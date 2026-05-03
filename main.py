from fastapi import FastAPI, Depends, HTTPException, APIRouter, Security
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, SecurityScopes
from sqlalchemy.orm import Session
from typing import List
from datetime import timedelta
from jose import JWTError, jwt
import models, schemas, crud, security
from db import SessionLocal, engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Mesa de Servicios Laboratorios",
    version = "0.1",
    description="API para gestión de tickets y servicios con JWT y Scopes"
)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="auth/token",
    scopes={
        "tickets:crear": "Crear nuevos tickets",
        "tickets:ver_propios": "Ver tickets propios",
        "tickets:recibir": "Cambiar estado a recibido",
        "tickets:asignar": "Asignar ticket",
        "tickets:atender": "Atender ticket",
        "tickets:finalizar": "Finalizar ticket",
        "tickets:ver_todos": "Ver todos los tickets",
        "usuarios:gestionar": "Gestionar usuarios"
    }
)

def get_current_user(security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Credenciales inválidas o token expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, security.SECRET_KEY, algorithms=[security.ALGORITHM])
        correo: str = payload.get("sub")
        if correo is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
    except JWTError:
        raise credentials_exception

    user = crud.get_usuario_by_correo(db, correo=correo)
    if user is None:
        raise credentials_exception

    for scope in security_scopes.scopes:
        if scope not in token_scopes:
            raise HTTPException(
                status_code=403,
                detail=f"Permiso denegado. Se requiere el scope: {scope}"
            )
    return user

router_usuarios = APIRouter(prefix="/usuarios", tags=["Usuarios"])
router_laboratorios = APIRouter(prefix="/laboratorios", tags=["Laboratorios"])
router_servicios = APIRouter(prefix="/servicios", tags=["Servicios"])
router_tickets = APIRouter(prefix="/tickets", tags=["Tickets"])

@app.post("/auth/token", tags=["Autenticación"])
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_usuario_by_correo(db, correo=form_data.username)
    
    if not user or not security.verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Correo o contraseña incorrectos")

    user_scopes = security.ROLE_SCOPES.get(user.rol, [])
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={
            "sub": user.correo,
            "id_usuario": user.id_usuario,
            "rol": user.rol,
            "scopes": user_scopes
        },
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router_usuarios.post("/", response_model=schemas.UsuarioOut)
def create_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db), current_user: models.Usuario = Security(get_current_user, scopes=["usuarios:gestionar"])):
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
def create_ticket(
    ticket: schemas.TicketCreate, 
    db: Session = Depends(get_db),
    current_user: models.Usuario = Security(get_current_user, scopes=["tickets:crear"])
):
    ticket.id_solicitante = current_user.id_usuario
    return crud.create_ticket(db, ticket)

@router_tickets.get("/", response_model=List[schemas.TicketOut])
def read_tickets(
    db: Session = Depends(get_db),
    current_user: models.Usuario = Security(get_current_user, scopes=["tickets:ver_todos", "tickets:ver_propios"])
):
    if current_user.rol == "admin":
        return crud.get_tickets(db)
    else:
        return crud.get_tickets(db)

@router_tickets.get("/{id_ticket}", response_model=schemas.TicketOut)
def read_ticket(
    id_ticket: int, 
    db: Session = Depends(get_db),
    current_user: models.Usuario = Security(get_current_user, scopes=["tickets:ver_todos", "tickets:ver_propios"])
):
    ticket = crud.get_ticket_by_id(db, id_ticket)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")
    return ticket

@router_tickets.patch("/{id_ticket}/estado", response_model=schemas.TicketOut)
def update_estado_ticket(
    id_ticket: int, 
    datos: schemas.TicketUpdateEstado, 
    db: Session = Depends(get_db),
    current_user: models.Usuario = Security(get_current_user, scopes=["tickets:recibir", "tickets:asignar", "tickets:atender", "tickets:finalizar"])
):
    ticket_actualizado = crud.update_ticket_estado(db, id_ticket, datos)
    if not ticket_actualizado:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")
    return ticket_actualizado

app.include_router(router_usuarios)
app.include_router(router_laboratorios)
app.include_router(router_servicios)
app.include_router(router_tickets)