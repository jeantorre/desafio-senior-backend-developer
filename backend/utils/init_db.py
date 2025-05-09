from database import Base, SessionLocal
from model import ModeloDocumento, ModeloTipoTransacao, ModeloTransporte
from sqlalchemy import text

from .seeds_db import (
    criar_documentos,
    criar_relacoes_usuario_documento,
    criar_tipo_transacao,
    criar_transportes,
    criar_usuarios,
)


def reset_db(engine) -> None:
    """
    Função responsável por resetar o banco de dados e alimentar com dados de teste

    param: engine: Engine
    return: None
    """
    try:
        with engine.connect() as connection:
            connection.execute(text("DROP SCHEMA public CASCADE;"))
            connection.execute(text("CREATE SCHEMA public;"))
            connection.commit()
        Base.metadata.create_all(bind=engine)
        db = SessionLocal()
        criar_tipo_transacao(db)
        criar_usuarios(db)
        criar_documentos(db)
        criar_relacoes_usuario_documento(db)
        criar_transportes(db)
        db.close()
        print("Banco de dados resetado com sucesso.")
    except Exception as e:
        print(f"Erro ao resetar o banco de dados: {e}")
        Base.metadata.create_all(bind=engine)


def init_prod_db(engine) -> None:
    """
    Função responsável por alimentar o banco de dados de produção com dados iniciais
    Inicializa apenas dados essenciais do sistema (tipos de transação, documentos e
      transportes)

    param: engine: Engine
    return: None
    """
    try:
        Base.metadata.create_all(bind=engine)
        db = SessionLocal()

        if not db.query(ModeloTipoTransacao).first():
            criar_tipo_transacao(db)
            print("Tipos de transação criados com sucesso")

        if not db.query(ModeloDocumento).first():
            criar_documentos(db)
            print("Documentos base criados com sucesso")

        if not db.query(ModeloTransporte).first():
            criar_transportes(db)
            print("Transportes base criados com sucesso")

        db.close()
        print("Inicialização do banco de dados de produção concluída com sucesso")
    except Exception as e:
        print(f"Erro ao inicializar o banco de dados de produção: {e}")
        raise
