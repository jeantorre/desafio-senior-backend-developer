import pytest
from database import Base, SessionLocal, engine, get_db
from fastapi.testclient import TestClient
from main import app
from sqlalchemy.orm import Session
from utils.init_db import reset_db
from utils.pydantic_validator import maiuscula_sem_acento


@pytest.fixture(scope="session", autouse=True)
def teste_db():
    """
    Teste de criação e exclusão de tabelas no banco de dados
    """
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    reset_db(engine)


@pytest.fixture(scope="function")
def db():
    """
    Teste de rollback no banco de dados
    """
    conexao = engine.connect()
    transacao = conexao.begin()
    sessao = SessionLocal(bind=conexao)

    yield sessao

    sessao.close()
    transacao.rollback()
    conexao.close()


@pytest.fixture
def cliente(db: Session):
    """
    Cria um cliente de teste com uma sessão de banco de dados
    """

    def sobrepor_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = sobrepor_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def test_dados_usuarios():
    return {
        "nome_usuario": maiuscula_sem_acento("Usuario Teste"),
        "email_usuario": "teste@teste.com",
        "senha": "123456",
    }


@pytest.fixture
def test_dados_documento():
    return {
        "descricao_documento": "Carteira de Identidade",
        "sigla_documento": "RG",
    }


@pytest.fixture
def test_transacao_data():
    return {
        "valor_transacao": 50.0,
        "tipo_transacao_id": "1",
        "transporte_id": "1",
    }
