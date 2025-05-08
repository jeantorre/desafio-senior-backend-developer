from fastapi import HTTPException
from model import ModeloDocumento, ModeloRlUsuarioDocumento
from schema import LerDocumento
from sqlalchemy.orm import Session


def ler_rl_usuario_documentos(
    db: Session,
    usuario_id: str,
) -> list[LerDocumento]:
    """
    Função responsável por listar todos os documentos de um usuário específico

    param: db: Session
    param: usuario_id: str
    return: list[LerDocumento]
    """
    documentos = (
        db.query(ModeloDocumento, ModeloRlUsuarioDocumento.saldo)
        .join(
            ModeloRlUsuarioDocumento,
            ModeloRlUsuarioDocumento.documento_id == ModeloDocumento.documento_id,
        )
        .filter(ModeloRlUsuarioDocumento.usuario_id == usuario_id)
        .all()
    )

    if not documentos:
        raise HTTPException(
            status_code=404,
            detail=f"Nenhum documento encontrado para o usuário {usuario_id}",
        )

    resultado = []
    for doc, saldo in documentos:
        resultado.append(
            {
                "documento_id": doc.documento_id,
                "descricao_documento": doc.descricao_documento,
                "sigla_documento": doc.sigla_documento,
                "saldo": saldo,
            }
        )

    return resultado
