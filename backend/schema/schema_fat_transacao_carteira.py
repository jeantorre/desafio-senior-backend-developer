from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class TransacaoCarteiraBase(BaseModel):
    """
    Schema que representa o modelo de transação de carteira

    Attributes:
        transacao_id (str): Identificador único da transação
        usuario_id (str): Identificador único do usuário
        documento_id (str): Identificador único do documento
        tipo_transacao_id (str): Identificador único do tipo de transação
        valor_transacao (decimal): Valor da transação
        data_transacao (datetime): Data e hora da transação
    """

    usuario_id: str = Field(..., description="Identificador único do usuário")
    documento_id: str = Field(..., description="Identificador único do documento")
    tipo_transacao_id: str = Field(
        ..., description="Identificador único do tipo de transação"
    )
    valor_transacao: Decimal = Field(..., description="Valor da transação")


class LerTransacaoCarteira(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    transacao_id: str
    usuario_id: str
    documento_id: str
    tipo_transacao_id: str
    valor_transacao: Decimal
    data_transacao: datetime


class CriarTransacaoCarteira(TransacaoCarteiraBase):
    pass
