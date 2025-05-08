import uuid
from datetime import datetime
from decimal import Decimal
from typing import Optional

from database import Base
from pytz import timezone
from sqlalchemy import Column, DateTime, ForeignKey, Numeric, String


class ModeloRlUsuarioDocumento(Base):
    """
    Modelo que representa a relação entre usuários e documentos.

    Atributos:
        rel_usuario_documento_id (str): Identificador único da relação.
        usuario_id (str): ID do usuário.
        documento_id (str): ID do documento.
        data_cadastro (datetime): Data e hora do cadastro da relação.
        data_atualizacao (datetime): Data e hora da última atualização da relação.
    """

    __tablename__ = "rl_usuario_documento"
    __table_args__ = {
        "comment": "Modelo que representa a relação entre usuários e documentos."
    }

    rel_usuario_documento_id: str = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        comment="Identificador único da relação.",
    )
    usuario_id: str = Column(
        String(36),
        ForeignKey("dim_usuario.usuario_id", ondelete="CASCADE"),
        nullable=False,
        comment="ID do usuário.",
    )
    documento_id: str = Column(
        String(36),
        ForeignKey("dim_documento.documento_id", ondelete="CASCADE"),
        nullable=False,
        comment="ID do documento.",
    )
    saldo: Optional[Decimal] = Column(
        Numeric(10, 2), comment="Quando aplicável, representa o saldo do documento."
    )
    data_cadastro: datetime = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone("America/Sao_Paulo")),
        nullable=False,
        comment="Data e hora do cadastro da relação no sistema.",
    )
    data_atualizacao: datetime = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone("America/Sao_Paulo")),
        onupdate=lambda: datetime.now(timezone("America/Sao_Paulo")),
        nullable=False,
        comment="Data e hora da última atualização da relação no sistema.",
    )
