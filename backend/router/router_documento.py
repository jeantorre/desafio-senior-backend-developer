from typing import List, Optional

from crud import (
    associar_documento,
    associar_vale_transporte,
    criar_documento,
    deletar_documento,
    ler_documento,
    ler_documentos,
)
from database import get_db
from fastapi import APIRouter, Depends, HTTPException, Query
from schema import CriarDocumento, LerDocumento
from sqlalchemy.orm import Session
from utils.auth import get_usuario_atual, verificar_bearer_token

router_documento = APIRouter(
    prefix="/documento",
    responses={404: {"descricao": "Não encontrado"}},
    tags=["Documentos"],
)


@router_documento.get(
    "/",
    response_model=List[LerDocumento],
    summary="Listar todos os documentos",
    description="""
                    Retorna uma lista de todos os documentos cadastrados no sistema.
                    """,
    dependencies=[Depends(get_usuario_atual), Depends(verificar_bearer_token)],
)
async def get_documentos(
    db: Session = Depends(get_db),
    descricao_documento: Optional[str] = Query(
        None, description="Filtrar por descrição do documento"
    ),
):
    """
    Retorna uma lista de todos os documentos cadastrados no sistema.
    """
    try:
        db_documentos = ler_documentos(db=db, descricao_documento=descricao_documento)
        return db_documentos
    except HTTPException as e:
        if e.status_code == 404:
            raise HTTPException(status_code=404, detail="Documentos não encontrados")
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)


@router_documento.get(
    "/{id_documento}",
    response_model=LerDocumento,
    summary="Listar um documento específico",
    description="""
                    Retorna as informações detalhadas de um documento específico.
                    """,
    dependencies=[Depends(get_usuario_atual), Depends(verificar_bearer_token)],
    include_in_schema=False,
)
async def get_documento(
    id_documento: str,
    db: Session = Depends(get_db),
):
    """
    Retorna as informações detalhadas de um documento específico.
    """
    try:
        db_documento = ler_documento(db=db, documento_id=id_documento)
        return db_documento
    except HTTPException as e:
        if e.status_code == 404:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)


@router_documento.post(
    "/registrar",
    response_model=LerDocumento,
    summary="Registrar um novo documento",
    description="""
                    Registra um novo documento no sistema.
                    """,
    dependencies=[Depends(get_usuario_atual), Depends(verificar_bearer_token)],
)
async def post_documento(
    documento: CriarDocumento,
    db: Session = Depends(get_db),
):
    try:
        db_documento = criar_documento(db=db, documento=documento)
        return db_documento
    except HTTPException as e:
        if e.status_code == 404:
            raise HTTPException(status_code=404, detail="Erro ao registrar documento")
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)


@router_documento.delete(
    "/{id_documento}",
    response_model=LerDocumento,
    summary="Deletar um documento existente",
    description="""
                              Deleta um estabelecimento existente do sistema.
                              """,
    dependencies=[Depends(get_usuario_atual), Depends(verificar_bearer_token)],
)
async def delete_documento(
    id_documento: str,
    db: Session = Depends(get_db),
):
    """
    Deleta um documento existente do sistema.
    """
    try:
        documento = ler_documento(db=db, documento_id=id_documento)
        if documento is None:
            raise HTTPException(status_code=404, detail="Documento não encontrado")
        db_documento = deletar_documento(db=db, documento_id=id_documento)
        return db_documento
    except HTTPException as e:
        if e.status_code == 404:
            raise HTTPException(status_code=404, detail="Documento não encontrado")
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)


@router_documento.post(
    "/associa_vt/{id_usuario}",
    response_model=LerDocumento,
    summary="Associar vale transporte a um usuário",
    description="""
                    Associa um documento de vale transporte a um usuário.
                    O saldo inicial será zero.
                    """,
    dependencies=[Depends(get_usuario_atual), Depends(verificar_bearer_token)],
)
async def associa_vale_transporte(
    id_usuario: str,
    db: Session = Depends(get_db),
):
    """
    Associa um documento de vale transporte a um usuário. O saldo inicial será zero.
    """
    try:
        relacao = associar_vale_transporte(db=db, usuario_id=id_usuario)
        documento = ler_documento(db=db, documento_id=relacao.documento_id)
        return {
            "documento_id": documento.documento_id,
            "descricao_documento": documento.descricao_documento,
            "sigla_documento": documento.sigla_documento,
            "saldo": relacao.saldo,
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router_documento.post(
    "/associa_documento/{id_usuario}",
    response_model=LerDocumento,
    summary="Associar documento a um usuário",
    description="""
                    Associa um documento a um usuário.
                    """,
    dependencies=[Depends(get_usuario_atual), Depends(verificar_bearer_token)],
)
async def associa_documento(
    id_usuario: str,
    documento_id: str = Query(..., description="ID do documento a ser associado"),
    db: Session = Depends(get_db),
):
    """
    Associa um documento a um usuário.
    """
    try:
        relacao = associar_documento(
            db=db, usuario_id=id_usuario, documento_id=documento_id
        )
        documento = ler_documento(db=db, documento_id=relacao.documento_id)
        return {
            "documento_id": documento.documento_id,
            "descricao_documento": documento.descricao_documento,
            "sigla_documento": documento.sigla_documento,
            "saldo": relacao.saldo,
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
