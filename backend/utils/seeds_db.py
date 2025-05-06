from model import ModeloUsuario
from schema import UsuarioBase
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
