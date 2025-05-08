import uuid
from datetime import datetime

from database import Base
from passlib.context import CryptContext
from pytz import timezone
from sqlalchemy import Column, DateTime, String

pwd_contexto = CryptContext(schemes=["bcrypt"], deprecated="auto")


class ModeloUsuario(Base):
    """
    Modelo que representa um estabelecimento.

    Atributos:
        usuario_id (str): Identificador único do usuário.
        nome (str): Nome do usuário.
        email (str): Email do usuário.
        data_cadastro (datetime): Data e hora do cadastro do usuário.
        data_atualizacao (datetime): Data e hora da última
        atualização do usuário.
    """

    __tablename__ = "dim_usuario"
    __table_args__ = {"comment": ("Modelo que representa um usuário do sistema.")}

    usuario_id: str = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        comment="Identificador único do usuário.",
    )
    nome_usuario: str = Column(String, comment="Nome do usuário.")
    email_usuario: str = Column(String, comment="Email do usuário.")
    senha: str = Column(String, comment="Hash da senha do usuário.")
    data_cadastro: datetime = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone("America/Sao_Paulo")),
        nullable=False,
        comment="Data e hora do cadastro do usuário no sistema.",
    )
    data_atualizacao: datetime = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone("America/Sao_Paulo")),
        onupdate=lambda: datetime.now(timezone("America/Sao_Paulo")),
        nullable=False,
        comment="Data e hora da última atualização do usuário no sistema.",
    )

    @staticmethod
    def verificar_senha(senha: str, senha_hash: str) -> bool:
        return pwd_contexto.verify(senha, senha_hash)

    @staticmethod
    def gerar_senha_hash(senha: str) -> str:
        return pwd_contexto.hash(senha)
