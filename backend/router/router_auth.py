from datetime import timedelta

from crud import validar_senha, validar_usuario_por_email
from database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError, jwt
from model import ModeloUsuario
from schema import Token
from sqlalchemy.orm import Session
from utils.auth import ALGORITHM, SECRET_KEY, criar_token_acesso, oauth2_scheme

router_auth = APIRouter(prefix="/auth", tags=["Autenticação"])

ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7


@router_auth.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    usuario = validar_usuario_por_email(db, form_data.username)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email não encontrado",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not validar_senha(usuario, form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Senha incorreta",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = criar_token_acesso(
        dados_usuario={"sub": usuario.cpf}, tempo_expiracao=access_token_expires
    )

    refresh_token_expires = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    refresh_token = criar_token_acesso(
        dados_usuario={"sub": usuario.cpf, "token_type": "refresh"},
        tempo_expiracao=refresh_token_expires,
    )

    return {
        "token_acesso": access_token,
        "token_refresh": refresh_token,
        "tipo_token": "bearer",
    }


@router_auth.post("/refresh-token", response_model=Token, include_in_schema=False)
async def refresh_token(
    current_token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    try:
        payload = jwt.decode(current_token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("token_type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Token inválido"
            )

        cpf: str = payload.get("sub")
        usuario = db.query(ModeloUsuario).filter(ModeloUsuario.cpf == cpf).first()

        access_token = criar_token_acesso(
            dados_usuario={
                "sub": usuario.cpf,
                "token_type": "access",
            }
        )

        return {
            "token_acesso": access_token,
            "token_refresh": current_token,
            "tipo_token": "bearer",
        }
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expirado ou inválido",
        )
