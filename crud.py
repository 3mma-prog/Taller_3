from sqlalchemy.orm import Session
import models, schemas, security

def get_usuarios(db: Session):
    return db.query(models.Usuario).all()

def get_usuario_by_id(db: Session, id_usuario: int):
    return db.query(models.Usuario).filter(models.Usuario.id_usuario == id_usuario).first()

def create_usuario(db: Session, usuario: schemas.UsuarioCreate):
    hashed_password = security.get_password_hash(usuario.password)
    nuevo_usuario = models.Usuario(
        nombre=usuario.nombre,
        correo=usuario.correo,
        password_hash=hashed_password, 
        rol=usuario.rol,
        activo=usuario.activo
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario

def get_laboratorios(db: Session):
    return db.query(models.Laboratorio).all()

def get_laboratorio_by_id(db: Session, id_laboratorio: int):
    return db.query(models.Laboratorio).filter(models.Laboratorio.id_laboratorio == id_laboratorio).first()

def create_laboratorio(db: Session, laboratorio: schemas.LaboratorioCreate):
    nuevo_laboratorio = models.Laboratorio(
        nombre=laboratorio.nombre,
        ubicacion=laboratorio.ubicacion,
        activo=laboratorio.activo
    )
    db.add(nuevo_laboratorio)
    db.commit()
    db.refresh(nuevo_laboratorio)
    return nuevo_laboratorio

def get_servicios(db: Session):
    return db.query(models.Servicio).all()

def get_servicio_by_id(db: Session, id_servicio: int):
    return db.query(models.Servicio).filter(models.Servicio.id_servicio == id_servicio).first()

def create_servicio(db: Session, servicio: schemas.ServicioCreate):
    nuevo_servicio = models.Servicio(
        nombre=servicio.nombre,
        descripcion=servicio.descripcion,
        activo=servicio.activo
    )
    db.add(nuevo_servicio)
    db.commit()
    db.refresh(nuevo_servicio)
    return nuevo_servicio

def get_tickets(db: Session):
    return db.query(models.Ticket).all()

def get_ticket_by_id(db: Session, id_ticket: int):
    return db.query(models.Ticket).filter(models.Ticket.id_ticket == id_ticket).first()

def create_ticket(db: Session, ticket: schemas.TicketCreate):
    nuevo_ticket = models.Ticket(
        id_solicitante=ticket.id_solicitante,
        id_laboratorio=ticket.id_laboratorio,
        id_servicio=ticket.id_servicio,
        titulo=ticket.titulo,
        descripcion=ticket.descripcion,
        prioridad=ticket.prioridad,
        estado="solicitado"
    )
    db.add(nuevo_ticket)
    db.commit()
    db.refresh(nuevo_ticket)
    return nuevo_ticket

def update_ticket_estado(db: Session, id_ticket: int, datos: schemas.TicketUpdateEstado):
    ticket = db.query(models.Ticket).filter(models.Ticket.id_ticket == id_ticket).first()
    
    if ticket is None:
        return None

    if datos.estado is not None:
        ticket.estado = datos.estado
        
    if datos.observacion_responsable is not None:
        ticket.observacion_responsable = datos.observacion_responsable
        
    if datos.observacion_tecnico is not None:
        ticket.observacion_tecnico = datos.observacion_tecnico

    db.commit()
    db.refresh(ticket)
    return ticket

    def get_usuario_by_correo(db: Session, correo: str):
    return db.query(models.Usuario).filter(models.Usuario.correo == correo).first()