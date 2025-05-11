from datetime import timedelta

from crud import validar_senha, validar_usuario_por_email
from database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from schema import Token
from sqlalchemy.orm import Session
from utils.auth import criar_token_acesso

router_auth = APIRouter(prefix="/auth", tags=["Autenticação"])

EXPIRA_TOKEN_ACESSO_MINUTOS = 30
EXPIRA_TOKEN_REFRESH_DIAS = 7


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

    expira_token_acesso = timedelta(minutes=EXPIRA_TOKEN_ACESSO_MINUTOS)
    token_acesso = criar_token_acesso(
        dados_usuario={"sub": usuario.email_usuario}, tempo_expiracao=expira_token_acesso
    )

    refresh_token_expires = timedelta(days=EXPIRA_TOKEN_REFRESH_DIAS)
    token_refresh = criar_token_acesso(
        dados_usuario={"sub": usuario.email_usuario, "token_type": "refresh"},
        tempo_expiracao=refresh_token_expires,
    )

    return {
        "token_acesso": token_acesso,
        "token_refresh": token_refresh,
        "tipo_token": "bearer",
    }
