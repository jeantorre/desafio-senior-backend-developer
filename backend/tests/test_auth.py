import pytest
from crud import criar_usuario
from fastapi.testclient import TestClient
from model import ModeloUsuario
from schema import CriarUsuario
from sqlalchemy.orm import Session


def test_criar_usuario(db: Session, test_user_data):
    """
    Teste para criar um usuário
    """

    user = CriarUsuario(**test_user_data)
    db_user = criar_usuario(db=db, usuario=user)

    assert db_user is not None
    assert db_user.nome_usuario == test_user_data["nome_usuario"]
    assert db_user.email_usuario == test_user_data["email_usuario"]
    assert db_user.senha != test_user_data["senha"]
    assert ModeloUsuario.verificar_senha(test_user_data["senha"], db_user.senha)


def test_registrar_usuario_via_api(client: TestClient, test_user_data):
    """Test user registration endpoint"""
    response = client.post("/usuario/registrar", json=test_user_data)

    assert response.status_code == 200
    data = response.json()
    assert data["nome_usuario"] == test_user_data["nome_usuario"]
    assert data["email_usuario"] == test_user_data["email_usuario"]
    assert "usuario_id" in data
    assert "senha" not in data  # Ensure password is not returned


def test_registrar_usuario_email_duplicado(client: TestClient, test_user_data):
    """Test registering a user with duplicate email"""
    # Register first user
    response = client.post("/usuario/registrar", json=test_user_data)
    assert response.status_code == 200

    # Try to register user with same email
    response = client.post("/usuario/registrar", json=test_user_data)
    assert response.status_code == 400
    assert "Email já cadastrado" in response.json()["detail"]


def test_login_usuario(client: TestClient, test_user_data):
    """Test user login"""
    # First register a user
    client.post("/usuario/registrar", json=test_user_data)

    # Try to login
    login_data = {
        "username": test_user_data["email_usuario"],
        "password": test_user_data["senha"],
    }

    response = client.post("/auth/login", data=login_data)

    assert response.status_code == 200
    data = response.json()
    assert "token_acesso" in data
    assert "token_refresh" in data


def test_login_usuario_credenciais_invalidas(client: TestClient, test_user_data):
    """Test login with invalid credentials"""
    # First register a user
    client.post("/usuario/registrar", json=test_user_data)

    # Try to login with wrong password
    login_data = {
        "username": test_user_data["email_usuario"],
        "password": "wrong_password",
    }

    response = client.post("/auth/login", data=login_data)

    assert response.status_code == 401
    assert "Credenciais inválidas" in response.json()["detail"]
