from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator
from utils.pydantic_validator import maiuscula_sem_acento


class TransporteBase(BaseModel):
    """
    Schema que representa o modelo de transporte

    Attributes:
        transporte_id (str): Identificador único do transporte
        descricao_transporte (str): Descrição do transporte
        valor_passagem (decimal): Valor da passagem
    """

    descricao_transporte: str = Field(..., description="Descrição do transporte")
    valor_passagem: Optional[Decimal] = Field(None, description="Valor da passagem")

    _normalizacao_strings_ = field_validator("descricao_transporte", mode="before")(
        maiuscula_sem_acento
    )


class LerTransporte(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    transporte_id: str
    descricao_transporte: str
    valor_passagem: Optional[Decimal]


class CriarTransporte(TransporteBase):
    pass
