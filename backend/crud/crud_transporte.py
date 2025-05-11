from typing import Optional

from fastapi import HTTPException
from model import ModeloTransporte
from schema import CriarTransporte, LerTransporte
from sqlalchemy.orm import Session


def get_transporte_descricao(db: Session, descricao_transporte: str) -> None:
    """
    Função responsável por buscar um transporte pela descrição

    param: db: Session
    param: descricao_transporte: str
    return: None
    """
    return (
        db.query(ModeloTransporte)
        .filter(ModeloTransporte.descricao_transporte == descricao_transporte)
        .first()
    )


def criar_transporte(db: Session, transporte: CriarTransporte) -> None:
    """
    Função responsável por criar um novo transporte ao sistema

    param: db: Session
    param: transporte: CriarTransporte
    return: None
    """
    if get_transporte_descricao(db, transporte.descricao_transporte):
        raise HTTPException(status_code=400, detail="Transporte já cadastrado")

    db_transporte = ModeloTransporte(**transporte.model_dump())

    db.add(db_transporte)
    db.commit()
    db.refresh(db_transporte)
    return db_transporte


def ler_transportes(
    db: Session,
    descricao_transporte: Optional[str] = None,
) -> list[LerTransporte]:
    """
    Função responsável por listar todos os transportes cadastrados no sistema

    param: db: Session
    param: descricao_transporte: Optional[str]
    return: list[LerTransporte]
    """
    query = db.query(ModeloTransporte)
    if descricao_transporte:
        query = query.filter(
            ModeloTransporte.descricao_transporte.ilike(f"%{descricao_transporte}%")
        )
    transportes = query.all()
    if not transportes:
        raise HTTPException(status_code=404, detail="Sem transportes cadastrados")
    return transportes


def ler_transporte(db: Session, transporte_id: str) -> LerTransporte:
    """
    Função responsável por listar um transporte específico cadastrado no sistema

    param: db: Session
    param: transporte_id: str
    return: LerTransporte
    """
    db_transporte = (
        db.query(ModeloTransporte)
        .filter(ModeloTransporte.transporte_id == transporte_id)
        .first()
    )
    if not db_transporte:
        raise HTTPException(status_code=404, detail="Transporte não encontrado")
    return db_transporte


def deletar_transporte(db: Session, transporte_id: str) -> None:
    """
    Função responsável por deletar um transporte específico cadastrado no sistema

    param: db: Session
    param: transporte_id: str
    return: None
    """
    db_transporte = (
        db.query(ModeloTransporte)
        .filter(ModeloTransporte.transporte_id == transporte_id)
        .first()
    )
    if not db_transporte:
        raise HTTPException(status_code=404, detail="Transporte não encontrado")
    db.delete(db_transporte)
    db.commit()

    return db_transporte
