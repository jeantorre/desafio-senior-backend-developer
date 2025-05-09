from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator
from utils.pydantic_validator import maiuscula_sem_acento


class DocumentoBase(BaseModel):
    """
    Schema que representa o modelo de documento

    Attributes:
        documento_id (str): Identificador único do documento
        descricao_documento (str): Descrição do documento
    """

    descricao_documento: str = Field(..., description="Descrição do documento")
    sigla_documento: Optional[str] = Field(None, description="Sigla do documento")

    _normalizacao_strings_ = field_validator(
        "descricao_documento", "sigla_documento", mode="before"
    )(maiuscula_sem_acento)


class LerDocumento(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    documento_id: str
    descricao_documento: str
    sigla_documento: Optional[str]


class CriarDocumento(DocumentoBase):
    pass
