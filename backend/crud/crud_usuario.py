from datetime import datetime
from typing import Optional

from fastapi import HTTPException
from model import ModeloUsuario
from pytz import timezone
from schema import AtualizarUsuario, CriarUsuario, LerUsuario
from sqlalchemy.orm import Session


def get_usuario_email(db: Session, email: str) -> None:
    """
    Retorna o e-mail do usuário informado

    param: db: Session
    param: email: str
    return: None
    """
    return db.query(ModeloUsuario).filter(ModeloUsuario.email_usuario == email).first()


def get_usuario_cpf(db: Session, cpf: str) -> None:
    """
    Retorna o CPF do usuário informado

    param: db: Session
    param: cpf: str
    return: None
    """
    return db.query(ModeloUsuario).filter(ModeloUsuario.cpf == cpf).first()


def validar_usuario_por_email(db: Session, email: str) -> None:
    """
    Valida se existe um usuário com o email informado para realizar o login

    param: db: Session
    param: email: str
    return: None
    """
    usuario = get_usuario_email(db, email)
    return usuario


def validar_senha(usuario: ModeloUsuario, senha: str) -> None:
    """
    Valida se a senha informada corresponde a senha armazenada

    param: usuario: ModeloUsuario
    param: senha: str
    return: None
    """
    return ModeloUsuario.verificar_senha(senha, usuario.senha)


def criar_usuario(db: Session, usuario: CriarUsuario) -> None:
    """
    Função responsável por criar um novo usuário ao sistema

    param: db: Session
    param: usuario: CriarUsuario
    return: None
    """
    if get_usuario_email(db, usuario.email_usuario):
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    senha_hash = ModeloUsuario.gerar_senha_hash(usuario.senha)
    db_usuario = ModeloUsuario(**usuario.model_dump(exclude={"senha"}), senha=senha_hash)

    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario


def ler_usuarios(
    db: Session,
    nome: Optional[str] = None,
) -> list[LerUsuario]:
    """
    Função responsável por listar todos os usuários cadastrados no sistema

    param: db: Session
    param: nome: Optional[str]
    return: list[LerUsuario]
    """
    query = db.query(ModeloUsuario)
    if nome:
        query = query.filter(ModeloUsuario.nome_usuario.ilike(f"%{nome}%"))
    usuarios = query.all()
    if not usuarios:
        raise HTTPException(status_code=404, detail="Sem usuários cadastrados")
    return usuarios


def ler_usuario(db: Session, usuario_id: str) -> LerUsuario:
    """
    Função responsável por listar um usuário específico cadastrado no sistema

    param: db: Session
    param: usuario_id: str
    return: LerUsuario
    """
    db_usuario = (
        db.query(ModeloUsuario).filter(ModeloUsuario.usuario_id == usuario_id).first()
    )
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return db_usuario


def atualizar_usuario(db: Session, usuario_id: str, usuario: AtualizarUsuario) -> None:
    """
    Função responsável por atualizar um usuário específico cadastrado no sistema

    param: db: Session
    param: usuario_id: str
    param: usuario: AtualizarUsuario
    return: None
    """
    db_usuario = (
        db.query(ModeloUsuario).filter(ModeloUsuario.usuario_id == usuario_id).first()
    )
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    if usuario.nova_senha is not None:
        if usuario.senha_atual is None:
            raise HTTPException(
                status_code=400,
                detail="Senha atual é obrigatória para atualizar a senha",
            )

        if not validar_senha(db_usuario, usuario.senha_atual):
            raise HTTPException(status_code=400, detail="Senha atual incorreta")

        db_usuario.senha = ModeloUsuario.gerar_senha_hash(usuario.nova_senha)

    db_usuario.data_atualizacao = datetime.now(timezone("America/Sao_Paulo"))
    db.commit()
    db.refresh(db_usuario)
    return db_usuario


def deletar_usuario(db: Session, usuario_id: str) -> None:
    """
    Função responsável por deletar um usuário específico cadastrado no sistema

    param: db: Session
    param: usuario_id: str
    return: None
    """
    db_usuario = (
        db.query(ModeloUsuario).filter(ModeloUsuario.usuario_id == usuario_id).first()
    )
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    db.delete(db_usuario)
    db.commit()

    return db_usuario
