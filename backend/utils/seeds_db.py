from model import ModeloDocumento, ModeloRlUsuarioDocumento, ModeloUsuario
from schema import DocumentoBase, UsuarioBase
from sqlalchemy.orm import Session


def criar_usuarios(db: Session) -> None:
    """
    Função responsável por criar usuários de teste no sistema

    param: db: Session
    return: None
    """
    usuarios = [
        {
            "nome_usuario": "Jãn Teste 1",
            "data_nascimento": "11/11/2011",
            "cpf": "00000000000",
            "telefone_usuario": "21999999999",
            "celular_usuario": "21999999999",
            "email_usuario": "teste1@teste.com",
            "senha": "teste1234",
        },
        {
            "nome_usuario": "Jãn Teste 2",
            "data_nascimento": "11/11/2011",
            "cpf": "11111111111",
            "telefone_usuario": "21999999999",
            "celular_usuario": "21999999999",
            "email_usuario": "teste2@teste.com",
            "senha": "teste1234",
        },
        {
            "nome_usuario": "Jãn Teste 3",
            "data_nascimento": "11/11/2011",
            "cpf": "22222222222",
            "telefone_usuario": "21999999999",
            "celular_usuario": "21999999999",
            "email_usuario": "teste3@teste.com",
            "senha": "teste1234",
        },
    ]

    try:
        db_usuarios = []
        for usuario in usuarios:
            senha_inicial = usuario.pop("senha")
            senha_hash = ModeloUsuario.gerar_senha_hash(senha_inicial)
            usuario["senha_hash"] = senha_hash
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
        {
            "descricao_documento": "Vale Transporte",
            "sigla_documento": "VT",
        },
        {
            "descricao_documento": "Vale Alimentação",
            "sigla_documento": "VA",
        },
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
                relacao = ModeloRlUsuarioDocumento(
                    usuario_id=usuario.usuario_id, documento_id=documento.documento_id
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
