from database import Base, SessionLocal
from sqlalchemy import text

from .seeds_db import (
    criar_documentos,
    criar_relacoes_usuario_documento,
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
        criar_usuarios(db)
        criar_documentos(db)
        criar_relacoes_usuario_documento(db)
        criar_transportes(db)
        db.close()
        print("Database reset successfully.")
    except Exception as e:
        print(f"Error resetting database: {e}")
        Base.metadata.create_all(bind=engine)
