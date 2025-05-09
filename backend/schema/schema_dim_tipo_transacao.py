from pydantic import BaseModel, Field, field_validator
from utils.pydantic_validator import maiuscula_sem_acento


class TipoTransacaoBase(BaseModel):
    """
    Schema que representa o modelo de tipo de transação

    Attributes:
        tipo_transacao_id (str): Identificador único do tipo de transação
        descricao_tipo_transacao (str): Descrição do tipo de transação
    """

    descricao_tipo_transacao: str = Field(
        ..., description="Descrição do tipo de transação"
    )

    _normalizacao_strings_ = field_validator("descricao_tipo_transacao", mode="before")(
        maiuscula_sem_acento
    )
