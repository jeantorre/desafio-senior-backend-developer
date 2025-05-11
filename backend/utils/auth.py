import os
from datetime import datetime, timedelta
from typing import Optional

from database import get_db
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, Security, status
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
    OAuth2PasswordBearer,
)
from jose import JWTError, jwt
from model import ModeloUsuario
from pytz import timezone
from sqlalchemy.orm import Session

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY não está definida.")
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
bearer_scheme = HTTPBearer()


def criar_token_acesso(dados_usuario: dict, tempo_expiracao: Optional[timedelta] = None):
    codificar = dados_usuario.copy()
    if tempo_expiracao:
        expire = datetime.now(timezone("America/Sao_Paulo")) + tempo_expiracao
    else:
        expire = datetime.now(timezone("America/Sao_Paulo")) + timedelta(minutes=15)
    codificar.update({"exp": expire})
    codificacao_jwt = jwt.encode(codificar, SECRET_KEY, algorithm=ALGORITHM)
    return codificacao_jwt


async def verificar_bearer_token(
    credentials: HTTPAuthorizationCredentials = Security(bearer_scheme),
):
    if credentials.scheme != "Bearer":
        raise HTTPException(status_code=401, detail="Token não fornecido")
    return credentials.credentials


async def get_usuario_atual(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    """
    Função responsável por obter o usuário atual a partir do token JWT

    param: token: str
    param: db: Session
    return: ModeloUsuario
    """
    credenciais_excecao = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email_usuario: str = payload.get("sub")
        if email_usuario is None:
            raise credenciais_excecao

        usuario = (
            db.query(ModeloUsuario)
            .filter(ModeloUsuario.email_usuario == email_usuario)
            .first()
        )
        if usuario is None:
            raise credenciais_excecao
        return usuario
    except JWTError:
        raise credenciais_excecao
