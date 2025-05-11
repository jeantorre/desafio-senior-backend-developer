import uuid

from database import Base
from sqlalchemy import Column, String


class ModeloTipoTransacao(Base):
    """
    Modelo que representa um tipo de transação.

    Atributos:
        tipo_transacao_id (str): Identificador único do tipo de transação.
        descricao_tipo_transacao (str): Descrição do tipo de transação.
    """

    __tablename__ = "dim_tipo_transacao"
    __table_args__ = {
        "comment": ("Modelo que representa um tipo de transação do sistema.")
    }

    tipo_transacao_id: str = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        comment="Identificador único da transação.",
    )
    descricao_tipo_transacao: str = Column(
        String,
        comment="Descrição do tipo de transação.",
    )
