from typing import Optional

from fastapi import HTTPException
from model import ModeloDocumento
from schema import CriarDocumento, LerDocumento
from sqlalchemy.orm import Session


def get_documento_descricao(db: Session, descricao_documento: str) -> None:
    """
    Função responsável por buscar um documento pela descrição

    param: db: Session
    param: descricao_documento: str
    return: None
    """
    return (
        db.query(ModeloDocumento)
        .filter(ModeloDocumento.descricao_documento == descricao_documento)
        .first()
    )


def criar_documento(db: Session, documento: CriarDocumento) -> None:
    """
    Função responsável por criar um novo documento ao sistema

    param: db: Session
    param: documento: CriarDocumento
    return: None
    """
    if get_documento_descricao(db, documento.descricao_documento):
        raise HTTPException(status_code=400, detail="Documento já cadastrada")

    db_documento = ModeloDocumento(**documento.model_dump())

    db.add(db_documento)
    db.commit()
    db.refresh(db_documento)
    return db_documento


def ler_documentos(
    db: Session,
    descricao_documento: Optional[str] = None,
) -> list[LerDocumento]:
    """
    Função responsável por listar todos os documentos cadastrados no sistema

    param: db: Session
    param: descricao_documento: Optional[str]
    return: list[LerDocumento]
    """
    query = db.query(ModeloDocumento)
    if descricao_documento:
        query = query.filter(
            ModeloDocumento.descricao_documento.ilike(f"%{descricao_documento}%")
        )
    documentos = query.all()
    if not documentos:
        raise HTTPException(status_code=404, detail="Sem documentos cadastrados")
    return documentos


def ler_documento(db: Session, documento_id: str) -> LerDocumento:
    """
    Função responsável por listar um documento específico cadastrado no sistema

    param: db: Session
    param: documento_id: str
    return: LerDocumento
    """
    db_documento = (
        db.query(ModeloDocumento)
        .filter(ModeloDocumento.documento_id == documento_id)
        .first()
    )
    if not db_documento:
        raise HTTPException(status_code=404, detail="Documento não encontrado")
    return db_documento


def deletar_documento(db: Session, documento_id: str) -> None:
    """
    Função responsável por deletar um documento específico cadastrado no sistema

    param: db: Session
    param: documento_id: str
    return: None
    """
    db_documento = (
        db.query(ModeloDocumento)
        .filter(ModeloDocumento.documento_id == documento_id)
        .first()
    )
    if not db_documento:
        raise HTTPException(status_code=404, detail="Documento não encontrado")
    db.delete(db_documento)
    db.commit()

    return db_documento
