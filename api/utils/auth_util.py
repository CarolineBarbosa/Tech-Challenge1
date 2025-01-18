import pandas as pd
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from api.database.db_connector import *
from api.Service import service
import api.Entidades.models as model

# Configurações do JWT
SECRET_KEY = "sua-chave-secreta"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Configurações para o gerenciamento de senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configuração do OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Usuário fake
"""
    username: FiapUser
    hashed_password: FIAP123
"""

# Verificar senha
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password: str):
    return pwd_context.hash(password)

# Função para autenticar o usuário
def authenticate_user(username: str, password: str):
    user = service.autenticar_usuario(username, password)

    #db_connector.DatabaseManager.read_to_dataframe
    #db_connector.
    #user = fake_users_db.get(username)
    if user.empty:
        return False
    if not verify_password(password, user.iloc[0]["Hashed_password"]):
        return False
    return user

# Função para criar o token JWT
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Função para obter o usuário atual a partir do token
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciais inválidas",
            )
        return username
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
        )
def cadastro(username: str, password: str) -> bool:
    data_user ={
        "User": [username],
        "Hashed_password": [hash_password(password)]
    }
    data_user = pd.DataFrame(data_user)
    db_manager = DatabaseManager()
    filters = [(model.Access.User == username)]
    if not db_manager.read_to_dataframe(model.Access, filters).empty:
        return False
    db_manager.insert_from_dataframe(model.Access, data_user)
    return True