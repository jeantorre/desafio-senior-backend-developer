from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator
from utils.pydantic_validator import maiuscula_sem_acento, validador_numero


class UsuarioBase(BaseModel):
    """
    Schema que representa o modelo de usuário

    Attributes:
        usuario_id (str): Identificador único do usuário
        nome_usuario (str): Nome do usuário
        data_nascimento (str): Data de nascimento do usuário
        cpf (str): CPF do usuário
        telefone_usuario (str): Telefone do usuário
        celular_usuario (str): Celular do usuário
        email_usuario (EmailStr): Email do usuário
        senha_hash (str): Senha hasheada do usuário
        data_cadastro (datetime): Data e hora do cadastro do usuário
        data_atualizacao (datetime): Data e hora da última
        atualização do usuário.
    """

    nome_usuario: str = Field(..., description="Nome do usuário")
    data_nascimento: str = Field(
        ..., description="Data de nascimento do usuário", pattern=r"^\d{2}/\d{2}/\d{4}$"
    )
    cpf: str = Field(..., description="CPF do usuário", pattern=r"^\d{11}$", unique=True)
    telefone_usuario: str = Field(..., description="Telefone do usuário")
    celular_usuario: str = Field(..., description="Celular do usuário")
    email_usuario: EmailStr = Field(..., description="Email do usuário")
    senha_hash: str = Field(..., description="Senha hasheada do usuário")

    _normalizacao_strings_ = field_validator("nome_usuario", mode="before")(
        maiuscula_sem_acento
    )
    _normalizacao_numeros_ = field_validator(
        "telefone_usuario", "celular_usuario", mode="before"
    )(validador_numero)

    @field_validator("data_nascimento")
    def validar_data_nascimento(cls, v):
        if not len(v) == 10:
            raise ValueError("Data de nascimento precisa conter 10 digitos")
        try:
            datetime.strptime(v, "%d/%m/%Y")
        except ValueError:
            raise ValueError("Formato de data inválido. Use DD/MM/YYYY")
        return v

    @field_validator("cpf")
    def validar_cpf(cls, v):
        if not v.isdigit() or len(v) != 11:
            raise ValueError("CPF precisa conter 11 digitos")
        return v


class UsuarioResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    usuario_id: str
    nome_usuario: str
    data_nascimento: str
    cpf: str
    telefone_usuario: str
    celular_usuario: str
    email_usuario: EmailStr
    data_cadastro: datetime
    data_atualizacao: datetime


class LerUsuario(UsuarioBase):
    model_config = ConfigDict(from_attributes=True)
    usuario_id: str
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
    model_config = ConfigDict(from_attributes=True, extra="forbid")
    telefone_usuario: Optional[str] = None
    celular_usuario: Optional[str] = None
    email_usuario: Optional[EmailStr] = None
    senha: Optional[str] = None

    _normalizacao_numeros_ = field_validator(
        "telefone_usuario", "celular_usuario", mode="before"
    )(validador_numero)
