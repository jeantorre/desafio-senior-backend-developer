import os
from datetime import datetime, timedelta
from typing import Optional

from database import get_db
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from model import ModeloUsuario
from sqlalchemy.orm import Session

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY não está definida.")
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def criar_token_acesso(dados_usuario: dict, tempo_expiracao: Optional[timedelta] = None):
    codificar = dados_usuario.copy()
    if tempo_expiracao:
        expire = datetime.utcnow() + tempo_expiracao
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    codificar.update({"exp": expire})
    codificacao_jwt = jwt.encode(codificar, SECRET_KEY, algorithm=ALGORITHM)
    return codificacao_jwt


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
        cpf: str = payload.get("sub")
        if cpf is None:
            raise credenciais_excecao

        usuario = db.query(ModeloUsuario).filter(ModeloUsuario.cpf == cpf).first()
        if usuario is None:
            raise credenciais_excecao
        return usuario
    except JWTError:
        raise credenciais_excecao
