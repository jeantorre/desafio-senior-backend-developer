import uuid
from datetime import datetime
from decimal import Decimal

from database import Base
from pytz import timezone
from sqlalchemy import Column, DateTime, ForeignKey, Numeric, String


class ModeloTransacaoCarteira(Base):
    """
    Modelo que representa uma transação de carteira.

    Atributos:
        transacao_id (str): Identificador único da transação.
        usuario_id (str): Identificador único do usuário.
        documento_id (str): Identificador único do documento.
        tipo_transacao_id (str): Identificador único do tipo de transação.
        valor_transacao (decimal): Valor da transação.
        data_transacao (datetime): Data e hora da transação.
    """

    __tablename__ = "fat_transacao_carteira"
    __table_args__ = {
        "comment": ("Modelo que representa uma transação de carteira do sistema.")
    }

    transacao_id: str = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        comment="Identificador único da transação.",
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
    tipo_transacao_id: str = Column(
        String,
        ForeignKey("dim_tipo_transacao.tipo_transacao_id", ondelete="CASCADE"),
        nullable=False,
        comment="ID do tipo de transação.",
    )
    valor_transacao: Decimal = Column(Numeric(10, 2), comment="Valor da transação.")
    data_transacao: datetime = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone("America/Sao_Paulo")),
        nullable=False,
        comment="Data e hora da transação.",
    )
