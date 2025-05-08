from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator
from utils.pydantic_validator import maiuscula_sem_acento


class UsuarioBase(BaseModel):
    """
    Schema que representa o modelo de usuário

    Attributes:
        usuario_id (str): Identificador único do usuário
        nome_usuario (str): Nome do usuário
        email_usuario (EmailStr): Email do usuário
        senha (str): Senha hasheada do usuário
        data_cadastro (datetime): Data e hora do cadastro do usuário
        data_atualizacao (datetime): Data e hora da última
        atualização do usuário.
    """

    nome_usuario: str = Field(..., description="Nome do usuário")
    email_usuario: EmailStr = Field(..., description="Email do usuário")
    senha: str = Field(..., description="Senha hasheada do usuário")

    _normalizacao_strings_ = field_validator("nome_usuario", mode="before")(
        maiuscula_sem_acento
    )


class LerUsuario(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    usuario_id: str
    nome_usuario: str
    email_usuario: EmailStr
    data_cadastro: datetime
    data_atualizacao: datetime


class CriarUsuario(UsuarioBase):
    pass


class AutenticarUsuario(BaseModel):
    cpf: str = Field(..., pattern=r"^\d{11}$")
    senha: str

    @field_validator("cpf")
    def validar_cpf(cls, v):
        if not v.isdigit() or len(v) != 11:
            raise ValueError("CPF precisa conter 11 digitos")
        return v


class Token(BaseModel):
    token_acesso: str
    token_refresh: str


class AtualizarUsuario(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    senha_atual: Optional[str] = None
    nova_senha: Optional[str] = None
