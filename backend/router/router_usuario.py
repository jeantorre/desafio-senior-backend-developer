from typing import List, Optional

from crud import (
    atualizar_usuario,
    criar_usuario,
    deletar_usuario,
    ler_usuario,
    ler_usuarios,
)
from database import get_db
from fastapi import APIRouter, Depends, HTTPException, Query
from schema import AtualizarUsuario, CriarUsuario, LerUsuario, UsuarioResponse
from sqlalchemy.orm import Session
from utils.auth import get_usuario_atual, verificar_bearer_token

router_usuario = APIRouter(
    prefix="/usuario",
    responses={404: {"descricao": "Não encontrado"}},
    tags=["Usuários"],
)


@router_usuario.get(
    "/",
    response_model=List[UsuarioResponse],
    summary="Listar todos os usuários",
    description="""
                    Retorna uma lista de todos os usuários cadastrados no sistema.
                    """,
    dependencies=[Depends(get_usuario_atual), Depends(verificar_bearer_token)],
)
async def get_usuarios(
    db: Session = Depends(get_db),
    nome: Optional[str] = Query(None, description="Filtrar por nome do usuário"),
):
    """
    Retorna uma lista de todos os usuários cadastrados no sistema.
    """
    try:
        db_usuarios = ler_usuarios(db=db, nome=nome)
        return db_usuarios
    except HTTPException as e:
        if e.status_code == 404:
            raise HTTPException(status_code=404, detail="Usuários não encontrado")
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)


@router_usuario.get(
    "/{id_usuario}",
    response_model=LerUsuario,
    summary="Listar um usuário específico",
    description="""
                    Retorna as informações detalhadas de um usuário específico.
                    """,
    dependencies=[Depends(get_usuario_atual), Depends(verificar_bearer_token)],
)
async def get_usuario(
    id_usuario: str,
    db: Session = Depends(get_db),
):
    """
    Retorna as informações detalhadas de um usuário específico.
    """
    try:
        db_usuario = ler_usuario(db=db, usuario_id=id_usuario)
        return db_usuario
    except HTTPException as e:
        if e.status_code == 404:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)


@router_usuario.post(
    "/registrar",
    response_model=LerUsuario,
    summary="Registrar um novo usuário",
    description="""
                    Registra um novo usuário no sistema.
                    """,
    dependencies=[Depends(get_usuario_atual), Depends(verificar_bearer_token)],
)
async def post_usuario(
    usuario: CriarUsuario,
    db: Session = Depends(get_db),
):
    try:
        db_usuario = criar_usuario(db=db, usuario=usuario)
        return db_usuario
    except HTTPException as e:
        if e.status_code == 404:
            raise HTTPException(status_code=404, detail="Erro ao registrar usuário")
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)


@router_usuario.put(
    "/{id_usuario}",
    response_model=LerUsuario,
    summary="Atualizar um usuário existente",
    description="""
                 Atualiza as informações de um usuário existente.
                 """,
    dependencies=[Depends(get_usuario_atual), Depends(verificar_bearer_token)],
)
async def update_usuario(
    id_usuario: str,
    usuario: AtualizarUsuario,
    db: Session = Depends(get_db),
):
    """
    Atualiza as informações de um usuário existente.
    Só podem ser atualizadas as informações de:
    - Telefone
    - Celular
    - Email
    - Senha
    """
    try:
        usuario_destino = ler_usuario(db=db, usuario_id=id_usuario)
        if usuario_destino is None:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        dados_atualizados = usuario.model_dump(exclude_unset=True)
        if not dados_atualizados:
            raise HTTPException(status_code=422, detail="Nenhum dado para atualizar")
        db_usuario = atualizar_usuario(db=db, usuario_id=id_usuario, usuario=usuario)
        return db_usuario
    except HTTPException as e:
        if e.status_code == 404:
            raise HTTPException(status_code=404, detail="Erro ao atualizar usuário")
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)


@router_usuario.delete(
    "/{id_usuario}",
    response_model=LerUsuario,
    summary="Deletar um usuário existente",
    description="""
                              Deleta um estabelecimento existente do sistema.
                              """,
    dependencies=[Depends(get_usuario_atual), Depends(verificar_bearer_token)],
)
async def delete_usuario(
    id_usuario: str,
    db: Session = Depends(get_db),
):
    """
    Deleta um usuário existente do sistema.
    """
    try:
        usuario = ler_usuario(db=db, usuario_id=id_usuario)
        if usuario is None:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        db_usuario = deletar_usuario(db=db, usuario_id=id_usuario)
        return db_usuario
    except HTTPException as e:
        if e.status_code == 404:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)
