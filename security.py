from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

if SECRET_KEY is None:
    raise RuntimeError("Falta configurar SECRET_KEY en el archivo .env")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

ROLE_SCOPES = {
    "solicitante": ["tickets:crear", "tickets:ver_propios"],
    "auxiliar": ["tickets:ver_propios", "tickets:atender"],
    "responsable_tecnico": [
        "tickets:ver_propios", 
        "tickets:recibir", 
        "tickets:asignar", 
        "tickets:finalizar"
    ],
    "tecnico_especializado": ["tickets:ver_propios", "tickets:atender"],
    "admin": [
        "tickets:crear", 
        "tickets:ver_propios", 
        "tickets:recibir", 
        "tickets:asignar", 
        "tickets:atender", 
        "tickets:finalizar", 
        "tickets:ver_todos", 
        "usuarios:gestionar"
    ]
}