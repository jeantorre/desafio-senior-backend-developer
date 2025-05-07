import uuid
from decimal import Decimal

from database import Base
from sqlalchemy import Column, Numeric, String


class ModeloTransporte(Base):
    """
    Modelo que representa um transporte.

    Atributos:
        transporte_id (str): Identificador único do transporte.
        descricao_transporte (str): Descrição do transporte.
        valor_passagem (decimal): Valor da passagem.
    """

    __tablename__ = "dim_transporte"
    __table_args__ = {"comment": ("Modelo que representa um transporte do sistema.")}

    transporte_id: str = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        comment="Identificador único do transporte.",
    )
    descricao_transporte: str = Column(String, comment="Descrição do transporte.")
    valor_passagem: Decimal = Column(Numeric(10, 2), comment="Valor da passagem.")
