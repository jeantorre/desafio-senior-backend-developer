from decimal import Decimal

from crud import criar_transacao_vale_transporte
from database import get_db
from fastapi import APIRouter, Depends, HTTPException, Query
from model import ModeloUsuario
from schema import CriarTransacaoCarteira, LerTransacaoCarteira
from sqlalchemy.orm import Session
from utils.auth import get_usuario_atual, verificar_bearer_token

router_transacao = APIRouter(
    prefix="/transacao",
    responses={404: {"descricao": "Não encontrado"}},
    tags=["Transações"],
)


@router_transacao.post(
    "/criar_transacao_vt/{id_usuario}",
    response_model=LerTransacaoCarteira,
    summary="Criar uma transação no vale transporte",
    description="""
                    Cria uma transação de vale transporte no sistema.
                    Tipos de transação:
                    - 1: Entrada - adiciona o valor correspondente ao saldo
                    - 2: Saída - subtrai o valor correspondente ao saldo, se houver saldo
                    suficiente
                    """,
    dependencies=[Depends(get_usuario_atual), Depends(verificar_bearer_token)],
)
async def post_transacao_carteira(
    id_usuario: str,
    valor_transacao: Decimal = Query(..., description="Valor da transação"),
    tipo_transacao: int = Query(
        ..., description="Tipo de transação (1=ENTRADA, 2=SAIDA)"
    ),
    db: Session = Depends(get_db),
):
    """
    Cria uma transação de vale transporte no sistema.
    """
    try:
        usuario = (
            db.query(ModeloUsuario)
            .filter(ModeloUsuario.usuario_id == id_usuario)
            .first()
        )
        if not usuario:
            raise HTTPException(
                status_code=404, detail=f"Usuário com ID {id_usuario} não encontrado"
            )

        if tipo_transacao not in [1, 2]:
            raise HTTPException(
                status_code=400,
                detail="Tipo de transação inválido. Use 1 para ENTRADA ou 2 para SAIDA",
            )

        tipo_transacao_str = "ENTRADA" if tipo_transacao == 1 else "SAIDA"

        transacao = CriarTransacaoCarteira(
            usuario_id=id_usuario,
            documento_id="",  # Será preenchido na função criar_transacao_vale_transporte
            valor_transacao=valor_transacao,
            tipo_transacao=tipo_transacao_str,
        )

        db_transacao = criar_transacao_vale_transporte(
            db=db, transacao_carteira=transacao
        )
        return db_transacao
    except HTTPException as e:
        if e.status_code == 404:
            raise HTTPException(status_code=404, detail=str(e.detail))
        if e.status_code == 400:
            raise HTTPException(status_code=400, detail=str(e.detail))
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
