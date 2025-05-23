from decimal import Decimal
from typing import Optional

from crud import criar_transacao_vale_transporte
from database import get_db
from fastapi import APIRouter, Depends, HTTPException, Query
from model import (
    ModeloDocumento,
    ModeloRlUsuarioDocumento,
    ModeloTipoTransacao,
    ModeloTransporte,
    ModeloUsuario,
)
from schema import CriarTransacaoCarteira, LerDocumentoComSaldo, LerTransacaoCarteira
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
    description=(
        "Cria uma transação de vale transporte no sistema. Tipos de transação:"
        "\n- 1: Entrada - adiciona o valor correspondente ao saldo"
        "\n- 2: Saída - subtrai o valor correspondente ao saldo, se houver "
        "saldo suficiente"
    ),
    dependencies=[Depends(get_usuario_atual), Depends(verificar_bearer_token)],
)
async def post_transacao_carteira(
    id_usuario: str,
    tipo_transacao: int = Query(
        ..., description="Tipo de transação (1=Entrada, 2=Saída)"
    ),
    tipo_transporte: Optional[int] = Query(
        None, description="Tipo de transporte (1=Ônibus, 2=Metrô, 3=Trem)"
    ),
    valor_transacao: Optional[Decimal] = Query(None, description="Valor da transação"),
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
        tipo_transacao_obj = (
            db.query(ModeloTipoTransacao)
            .filter(ModeloTipoTransacao.descricao_tipo_transacao == tipo_transacao_str)
            .first()
        )

        if not tipo_transacao_obj:
            raise HTTPException(
                status_code=404,
                detail=f"Tipo de transação {tipo_transacao_str} não encontrado",
            )

        if tipo_transacao == 1:
            if valor_transacao is None:
                raise HTTPException(
                    status_code=400,
                    detail=(
                        "Valor da transação é obrigatório para recarga do vale "
                        "transporte"
                    ),
                )
            if valor_transacao <= 0:
                raise HTTPException(
                    status_code=400,
                    detail="Valor da transação deve ser maior que 0",
                )

            transacao = CriarTransacaoCarteira(
                usuario_id=id_usuario,
                documento_id="",
                valor_transacao=valor_transacao,
                tipo_transacao_id=tipo_transacao_obj.tipo_transacao_id,
            )

            db_transacao = criar_transacao_vale_transporte(
                db=db, transacao_carteira=transacao
            )
            return db_transacao

        elif tipo_transacao == 2:
            if tipo_transporte is None:
                raise HTTPException(
                    status_code=400,
                    detail=(
                        "Tipo de transporte é obrigatório para saída do vale transporte"
                    ),
                )

            if tipo_transporte not in [1, 2, 3]:
                raise HTTPException(
                    status_code=400,
                    detail=(
                        "Tipo de transporte inválido. Use 1 para Ônibus, 2 para Metrô "
                        "ou 3 para Trem"
                    ),
                )

            tipo_transporte_str = (
                "ONIBUS"
                if tipo_transporte == 1
                else "METRO" if tipo_transporte == 2 else "TREM"
            )

            meio_transporte = (
                db.query(ModeloTransporte)
                .filter(ModeloTransporte.descricao_transporte == tipo_transporte_str)
                .first()
            )

            if not meio_transporte:
                raise HTTPException(
                    status_code=404,
                    detail=f"Transporte {tipo_transporte_str} não encontrado",
                )

            transacao = CriarTransacaoCarteira(
                usuario_id=id_usuario,
                documento_id="",
                valor_transacao=meio_transporte.valor_passagem,
                tipo_transacao_id=tipo_transacao_obj.tipo_transacao_id,
            )

            db_transacao = criar_transacao_vale_transporte(
                db=db, transacao_carteira=transacao
            )
            return db_transacao

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router_transacao.get(
    "/saldo_vt/{id_usuario}",
    response_model=LerDocumentoComSaldo,
    summary="Consultar saldo do vale transporte",
    description="""
                    Consulta o saldo atual do vale transporte de um usuário.
                    """,
    dependencies=[Depends(get_usuario_atual), Depends(verificar_bearer_token)],
)
async def get_saldo_vale_transporte(
    id_usuario: str,
    db: Session = Depends(get_db),
):
    """
    Consulta o saldo atual do vale transporte de um usuário.
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

        vale_transporte = (
            db.query(ModeloDocumento, ModeloRlUsuarioDocumento.saldo)
            .join(
                ModeloRlUsuarioDocumento,
                ModeloRlUsuarioDocumento.documento_id == ModeloDocumento.documento_id,
            )
            .filter(
                ModeloDocumento.descricao_documento == "VALE TRANSPORTE",
                ModeloRlUsuarioDocumento.usuario_id == id_usuario,
            )
            .first()
        )

        if not vale_transporte:
            raise HTTPException(
                status_code=404,
                detail="Vale transporte não encontrado para este usuário",
            )

        doc, saldo = vale_transporte
        return {
            "documento_id": doc.documento_id,
            "descricao_documento": doc.descricao_documento,
            "sigla_documento": doc.sigla_documento,
            "saldo": saldo,
        }

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
