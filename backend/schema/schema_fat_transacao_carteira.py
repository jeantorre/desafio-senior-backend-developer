from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, PositiveFloat


class TransacaoCarteiraBase(BaseModel):
    """
    Schema que representa o modelo de transação de carteira

    Attributes:
        transacao_id (str): Identificador único da transação
        usuario_id (str): Identificador único do usuário
        documento_id (str): Identificador único do documento
        valor_transacao (decimal): Valor da transação
        tipo_transacao (str): Tipo de transação
        data_hora_transacao (datetime): Data e hora da transação
    """

    usuario_id: str = Field(..., description="Identificador único do usuário")
    documento_id: str = Field(..., description="Identificador único do documento")
    valor_transacao: PositiveFloat = Field(..., description="Valor da transação")
    tipo_transacao: str = Field(..., description="Tipo de transação")
    data_hora_transacao: datetime = Field(..., description="Data e hora da transação")


class LerTransacaoCarteira(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    transacao_id: str
    usuario_id: str
    documento_id: str
    valor_transacao: Decimal
    tipo_transacao: str
    data_hora_transacao: datetime


class CriarTransacaoCarteira(TransacaoCarteiraBase):
    pass
