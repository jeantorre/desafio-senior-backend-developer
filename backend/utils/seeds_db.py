from model import (
    ModeloDocumento,
    ModeloRlUsuarioDocumento,
    ModeloTipoTransacao,
    ModeloTransporte,
    ModeloUsuario,
)
from schema import DocumentoBase, TipoTransacaoBase, TransporteBase, UsuarioBase
from sqlalchemy.orm import Session


def criar_tipo_transacao(db: Session) -> None:
    """
    Função responsável por criar tipos de transação no sistema

    param: db: Session
    return: None
    """
    tipo_transacoes = ["ENTRADA", "SAIDA", "ESTORNO"]
    try:
        db_tipo_transacoes = []
        for tipo_transacao in tipo_transacoes:
            tipo_transacao = TipoTransacaoBase(descricao_tipo_transacao=tipo_transacao)
            db_tipo_transacao = ModeloTipoTransacao(**tipo_transacao.model_dump())
            db.add(db_tipo_transacao)
            db_tipo_transacoes.append(db_tipo_transacao)
        db.commit()
        for db_tipo_transacao in db_tipo_transacoes:
            db.refresh(db_tipo_transacao)
        print("Tipos de transações criados com sucesso!")
    except Exception as e:
        print(f"Erro ao criar tipos de transações: {e}")
        db.rollback()


def criar_usuarios(db: Session) -> None:
    """
    Função responsável por criar usuários de teste no sistema

    param: db: Session
    return: None
    """
    usuarios = [
        {
            "nome_usuario": "Jãn Teste 1",
            "email_usuario": "teste1@teste.com",
            "senha": "teste1234",
        },
        {
            "nome_usuario": "Jãn Teste 2",
            "email_usuario": "teste2@teste.com",
            "senha": "teste1234",
        },
        {
            "nome_usuario": "Jãn Teste 3",
            "email_usuario": "teste3@teste.com",
            "senha": "teste1234",
        },
    ]

    try:
        db_usuarios = []
        for usuario in usuarios:
            senha_inicial = usuario.pop("senha")
            senha_hash = ModeloUsuario.gerar_senha_hash(senha_inicial)
            usuario["senha"] = senha_hash
            usuario = UsuarioBase(**usuario)
            db_usuario = ModeloUsuario(**usuario.model_dump())
            db.add(db_usuario)
            db_usuarios.append(db_usuario)
        db.commit()
        for db_usuario in db_usuarios:
            db.refresh(db_usuario)
        print("Usuários criados com sucesso!")
    except Exception as e:
        print(f"Erro ao criar usuários: {e}")
        db.rollback()


def criar_documentos(db: Session) -> None:
    """
    Função responsável por criar documentos de teste no sistema

    param: db: Session
    return: None
    """
    documentos = [
        {
            "descricao_documento": "Registro Geral",
            "sigla_documento": "RG",
        },
        {
            "descricao_documento": "Cadastro de Pessoa Física",
            "sigla_documento": "CPF",
        },
        {
            "descricao_documento": "Carteira Nacional de Habilitação",
            "sigla_documento": "CNH",
        },
        {"descricao_documento": "Vale Transporte", "sigla_documento": "VT"},
        {"descricao_documento": "Vale Alimentação", "sigla_documento": "VA"},
    ]

    try:
        db_documentos = []
        for documento in documentos:
            documento = DocumentoBase(**documento)
            db_documento = ModeloDocumento(**documento.model_dump())
            db.add(db_documento)
            db_documentos.append(db_documento)
        db.commit()
        for db_documento in db_documentos:
            db.refresh(db_documento)
        print("Documentos criados com sucesso!")
    except Exception as e:
        print(f"Erro ao criar documentos: {e}")
        db.rollback()


def criar_relacoes_usuario_documento(db: Session) -> None:
    """
    Função responsável por criar relações aleatórias entre usuários e documentos

    param: db: Session
    return: None
    """

    try:
        usuarios = db.query(ModeloUsuario).all()
        documentos = db.query(ModeloDocumento).all()

        relacoes = []
        for usuario in usuarios:
            for documento in documentos:
                if documento.descricao_documento == "VALE TRANSPORTE":
                    saldo = 10.00
                else:
                    saldo = None
                relacao = ModeloRlUsuarioDocumento(
                    usuario_id=usuario.usuario_id,
                    documento_id=documento.documento_id,
                    saldo=saldo,
                )
                db.add(relacao)
                relacoes.append(relacao)

        db.commit()
        for relacao in relacoes:
            db.refresh(relacao)
        print("Relações entre usuários e documentos criadas com sucesso!")
    except Exception as e:
        print(f"Erro ao criar relações entre usuários e documentos: {e}")
        db.rollback()


def criar_transportes(db: Session) -> None:
    """
    Função responsável por criar transportes de teste no sistema

    param: db: Session
    return: None
    """
    transportes = [
        {
            "descricao_transporte": "Trem",
            "valor_passagem": 7.60,
        },
        {
            "descricao_transporte": "Ônibus",
            "valor_passagem": 5.50,
        },
        {
            "descricao_transporte": "Metrô",
            "valor_passagem": 7.90,
        },
    ]

    try:
        db_transportes = []
        for transporte in transportes:
            transporte = TransporteBase(**transporte)
            db_transporte = ModeloTransporte(**transporte.model_dump())
            db.add(db_transporte)
            db_transportes.append(db_transporte)
        db.commit()
        for db_transporte in db_transportes:
            db.refresh(db_transporte)
        print("Transportes criados com sucesso!")
    except Exception as e:
        print(f"Erro ao criar documentos: {e}")
        db.rollback()
