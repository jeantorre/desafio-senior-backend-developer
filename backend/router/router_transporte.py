from typing import List, Optional

from crud import criar_transporte, deletar_transporte, ler_transporte, ler_transportes
from database import get_db
from fastapi import APIRouter, Depends, HTTPException, Query
from schema import CriarTransporte, LerTransporte
from sqlalchemy.orm import Session
from utils.auth import get_usuario_atual, verificar_bearer_token

router_transporte = APIRouter(
    prefix="/transporte",
    responses={404: {"descricao": "Não encontrado"}},
    tags=["Transportes"],
)


@router_transporte.get(
    "/",
    response_model=List[LerTransporte],
    summary="Listar todos os transportes",
    description="""
                    Retorna uma lista de todos os transportes cadastrados no sistema.
                    """,
    dependencies=[Depends(get_usuario_atual), Depends(verificar_bearer_token)],
)
async def get_documentos(
    db: Session = Depends(get_db),
    descricao_transporte: Optional[str] = Query(
        None, description="Filtrar por descrição do transporte"
    ),
):
    """
    Retorna uma lista de todos os transportes cadastrados no sistema.
    """
    try:
        db_transportes = ler_transportes(
            db=db, descricao_transporte=descricao_transporte
        )
        return db_transportes
    except HTTPException as e:
        if e.status_code == 404:
            raise HTTPException(status_code=404, detail="Documentos não encontrados")
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)


@router_transporte.get(
    "/{id_transporte}",
    response_model=LerTransporte,
    summary="Listar um transporte específico",
    description="""
                    Retorna as informações detalhadas de um transporte específico.
                    """,
    dependencies=[Depends(get_usuario_atual), Depends(verificar_bearer_token)],
)
async def get_transporte(
    id_transporte: str,
    db: Session = Depends(get_db),
):
    """
    Retorna as informações detalhadas de um transporte específico.
    """
    try:
        db_transporte = ler_transporte(db=db, transporte_id=id_transporte)
        return db_transporte
    except HTTPException as e:
        if e.status_code == 404:
            raise HTTPException(status_code=404, detail="Transporte não encontrado")
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)


@router_transporte.post(
    "/registrar",
    response_model=LerTransporte,
    summary="Registrar um novo transporte",
    description="""
                    Registra um novo transporte no sistema.
                    """,
    dependencies=[Depends(get_usuario_atual), Depends(verificar_bearer_token)],
)
async def post_transporte(
    transporte: CriarTransporte,
    db: Session = Depends(get_db),
):
    try:
        db_transporte = criar_transporte(db=db, transporte=transporte)
        return db_transporte
    except HTTPException as e:
        if e.status_code == 404:
            raise HTTPException(status_code=404, detail="Erro ao registrar transporte")
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)


@router_transporte.delete(
    "/{id_transporte}",
    response_model=LerTransporte,
    summary="Deletar um transporte existente",
    description="""
                              Deleta um estabelecimento existente do sistema.
                              """,
    dependencies=[Depends(get_usuario_atual), Depends(verificar_bearer_token)],
)
async def delete_transporte(
    id_transporte: str,
    db: Session = Depends(get_db),
):
    """
    Deleta um transporte existente do sistema.
    """
    try:
        transporte = ler_transporte(db=db, transporte_id=id_transporte)
        if transporte is None:
            raise HTTPException(status_code=404, detail="Transporte não encontrado")
        db_transporte = deletar_transporte(db=db, transporte_id=id_transporte)
        return db_transporte
    except HTTPException as e:
        if e.status_code == 404:
            raise HTTPException(status_code=404, detail="Transporte não encontrado")
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)
