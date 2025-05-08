import uuid
from typing import Optional

from database import Base
from sqlalchemy import Column, String


class ModeloDocumento(Base):
    """
    Modelo que representa um documento.

    Atributos:
        documento_id (str): Identificador único do documento.
        descricao_documento (str): Descrição do documento.
        sigla_documento (str): Sigla do documento.
    """

    __tablename__ = "dim_documento"
    __table_args__ = {"comment": ("Modelo que representa um documento do sistema.")}

    documento_id: str = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        comment="Identificador único do documento.",
    )
    descricao_documento: str = Column(String, comment="Descrição do documento.")
    sigla_documento: Optional[str] = Column(String, comment="Sigla do documento.")
