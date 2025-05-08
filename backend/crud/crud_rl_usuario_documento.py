from fastapi import HTTPException
from model import ModeloDocumento, ModeloRlUsuarioDocumento, ModeloUsuario
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


def associar_vale_transporte(db: Session, usuario_id: str) -> None:
    """
    Função responsável por associar um documento de vale transporte a um usuário

    param: db: Session
    param: usuario_id: str
    return: None
    """
    usuario = (
        db.query(ModeloUsuario).filter(ModeloUsuario.usuario_id == usuario_id).first()
    )
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    vale_transporte = (
        db.query(ModeloDocumento)
        .filter(ModeloDocumento.descricao_documento == "VALE TRANSPORTE")
        .first()
    )
    if not vale_transporte:
        raise HTTPException(
            status_code=404, detail="Documento de vale transporte não encontrado"
        )

    relacao_existente = (
        db.query(ModeloRlUsuarioDocumento)
        .filter(
            ModeloRlUsuarioDocumento.usuario_id == usuario_id,
            ModeloRlUsuarioDocumento.documento_id == vale_transporte.documento_id,
        )
        .first()
    )
    if relacao_existente:
        raise HTTPException(status_code=400, detail="Usuário já possui vale transporte")

    nova_relacao = ModeloRlUsuarioDocumento(
        usuario_id=usuario_id,
        documento_id=vale_transporte.documento_id,
        saldo=0.00,
    )
    db.add(nova_relacao)
    db.commit()
    db.refresh(nova_relacao)
    return nova_relacao
