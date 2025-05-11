from typing import Optional

from fastapi import HTTPException
from model import (
    ModeloDocumento,
    ModeloRlUsuarioDocumento,
    ModeloTipoTransacao,
    ModeloTransacaoCarteira,
    ModeloUsuario,
)
from schema import CriarTransacaoCarteira, LerTransacaoCarteira
from sqlalchemy.orm import Session


def criar_transacao_vale_transporte(
    db: Session, transacao_carteira: CriarTransacaoCarteira
) -> None:
    """
    Função responsável por criar uma nova transação de vale transporte e atualizar o
    saldo do vale transporte

    param: db: Session
    param: transacao_carteira: CriarTransacaoCarteira
    return: None
    """

    usuario = (
        db.query(ModeloUsuario)
        .filter(ModeloUsuario.usuario_id == transacao_carteira.usuario_id)
        .first()
    )

    if not usuario:
        raise HTTPException(
            status_code=404,
            detail=f"Usuário com ID {transacao_carteira.usuario_id} não encontrado",
        )

    vale_transporte = (
        db.query(ModeloDocumento)
        .filter(ModeloDocumento.descricao_documento == "VALE TRANSPORTE")
        .first()
    )

    vale_transporte_id = vale_transporte.documento_id

    vale_transporte = (
        db.query(ModeloRlUsuarioDocumento)
        .filter(
            ModeloRlUsuarioDocumento.usuario_id == transacao_carteira.usuario_id,
            ModeloRlUsuarioDocumento.documento_id == vale_transporte_id,
        )
        .first()
    )

    if not vale_transporte:
        raise HTTPException(status_code=404, detail="Vale transporte não encontrado")

    if vale_transporte.saldo is None:
        vale_transporte.saldo = 0

    tipo_transacao = (
        db.query(ModeloTipoTransacao)
        .filter(
            ModeloTipoTransacao.tipo_transacao_id == transacao_carteira.tipo_transacao_id
        )
        .first()
    )

    if not tipo_transacao:
        raise HTTPException(status_code=404, detail="Tipo de transação não encontrado")

    if tipo_transacao.descricao_tipo_transacao == "ENTRADA":
        vale_transporte.saldo += transacao_carteira.valor_transacao
    elif tipo_transacao.descricao_tipo_transacao == "SAIDA":
        if vale_transporte.saldo < transacao_carteira.valor_transacao:
            raise HTTPException(
                status_code=400, detail="Saldo insuficiente para realizar a transação"
            )
        vale_transporte.saldo -= transacao_carteira.valor_transacao
    else:
        raise HTTPException(
            status_code=400,
            detail="Tipo de transação inválido. Use 'ENTRADA' ou 'SAIDA'",
        )

    transacao_data = transacao_carteira.model_dump()
    transacao_data["documento_id"] = vale_transporte.documento_id

    db_transacao_carteira = ModeloTransacaoCarteira(**transacao_data)
    db.add(db_transacao_carteira)
    db.commit()
    db.refresh(db_transacao_carteira)
    return db_transacao_carteira


def ler_transacoes_carteira(
    db: Session,
    usuario_id: Optional[str] = None,
) -> list[LerTransacaoCarteira]:
    """
    Função responsável por listar todas as transações de carteira cadastradas no sistema

    param: db: Session
    param: usuario_id: Optional[str]
    return: list[LerTransacaoCarteira]
    """
    query = db.query(ModeloTransacaoCarteira)
    if usuario_id:
        query = query.filter(ModeloTransacaoCarteira.usuario_id == usuario_id)
    transacoes = query.all()
    if not transacoes:
        raise HTTPException(status_code=404, detail="Sem transações cadastradas")
    return transacoes


def ler_transacao_carteira(
    db: Session, transacao_carteira_id: str
) -> LerTransacaoCarteira:
    """
    Função responsável por listar uma transação de carteira específica cadastrada no
    sistema

    param: db: Session
    param: transacao_carteira_id: str
    return: LerTransacaoCarteira
    """
    db_transacao_carteira = (
        db.query(ModeloTransacaoCarteira)
        .filter(ModeloTransacaoCarteira.transacao_id == transacao_carteira_id)
        .first()
    )
    if not db_transacao_carteira:
        raise HTTPException(
            status_code=404, detail="Transação de carteira não encontrada"
        )
    return db_transacao_carteira


def deletar_transacao_carteira(db: Session, transacao_carteira_id: str) -> None:
    """
    Função responsável por deletar uma transação de carteira específica cadastrada no
    sistema.
    Apenas saídas podem ser estornadas, retornando o valor ao saldo.

    param: db: Session
    param: transacao_carteira_id: str
    return: None
    """
    db_transacao_carteira = (
        db.query(ModeloTransacaoCarteira)
        .filter(ModeloTransacaoCarteira.transacao_id == transacao_carteira_id)
        .first()
    )
    if not db_transacao_carteira:
        raise HTTPException(
            status_code=404, detail="Transação de carteira não encontrada"
        )

    tipo_transacao = (
        db.query(ModeloTipoTransacao)
        .filter(
            ModeloTipoTransacao.tipo_transacao_id
            == db_transacao_carteira.tipo_transacao_id
        )
        .first()
    )

    if tipo_transacao.descricao_tipo_transacao == "ENTRADA":
        raise HTTPException(
            status_code=400, detail="Não é possível estornar uma entrada"
        )

    documento = (
        db.query(ModeloDocumento)
        .filter(ModeloDocumento.documento_id == db_transacao_carteira.documento_id)
        .first()
    )

    if not documento:
        raise HTTPException(status_code=404, detail="Documento não encontrado")

    documento.saldo += db_transacao_carteira.valor_transacao

    tipo_transacao_estorno = (
        db.query(ModeloTipoTransacao)
        .filter(ModeloTipoTransacao.descricao_tipo_transacao == "ESTORNO")
        .first()
    )

    if not tipo_transacao_estorno:
        raise HTTPException(
            status_code=404, detail="Tipo de transação ESTORNO não encontrado"
        )

    estorno = ModeloTransacaoCarteira(
        usuario_id=db_transacao_carteira.usuario_id,
        documento_id=db_transacao_carteira.documento_id,
        valor_transacao=db_transacao_carteira.valor_transacao,
        tipo_transacao_id=tipo_transacao_estorno.tipo_transacao_id,
    )

    db.add(estorno)
    db.commit()

    return estorno
