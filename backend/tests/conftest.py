import os
import sys
from typing import Generator

import pytest
import utils.init_db
import utils.pydantic_validator
from database import Base
from fastapi.testclient import TestClient
from main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


os.environ["DATABASE_URL"] = "sqlite:///./test.db"


original_reset_db = utils.init_db.reset_db


def mock_reset_db(*args, **kwargs):
    pass


utils.init_db.reset_db = mock_reset_db


utils.init_db.reset_db = original_reset_db

TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def db() -> Generator[Session, None, None]:
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db: Session) -> Generator[TestClient, None, None]:
    app.dependency_overrides = {}
    app.dependency_overrides["database.get_db"] = lambda: db

    with TestClient(app) as c:
        yield c

    app.dependency_overrides = {}


@pytest.fixture
def test_user_data():
    return {
        "nome_usuario": utils.pydantic_validator.maiuscula_sem_acento("Usuario Teste"),
        "email_usuario": "teste@teste.com",
        "senha": "123456",
    }


@pytest.fixture
def test_documento_data():
    return {
        "tipo_documento": "RG",
        "numero_documento": "123456789",
        "data_expedicao": "2020-01-01",
        "orgao_expedidor": "SSP",
    }


@pytest.fixture
def test_transporte_data():
    return {"tipo_transporte": "ONIBUS", "numero_cartao": "1234567890", "saldo": 100.0}


@pytest.fixture
def test_transacao_data():
    return {
        "valor_transacao": 50.0,
        "tipo_transacao_id": "1",  # Assuming this ID exists
        "transporte_id": "1",  # Will be replaced in tests
    }
