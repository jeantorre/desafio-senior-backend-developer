import pytest
from crud import criar_usuario
from fastapi.testclient import TestClient
from model import ModeloUsuario
from schema import CriarUsuario
from sqlalchemy.orm import Session

def _criar_usuario_obter_token(cliente, test_user_data):
    """
    Cria um usuário teste e retorna um token de autenticação
    """
    response = cliente.post("/usuario/registrar", json=test_user_data)
    usuario_id = response.json()["usuario_id"]

    login_data = {
        "username": test_user_data["email_usuario"],
        "password": test_user_data["senha"],
    }

    response = cliente.post("/auth/login", data=login_data)
    token = response.json()["token_acesso"]

    return usuario_id, token


def test_criar_usuario(db: Session, test_dados_usuarios):
    """
    Teste para criar um usuário
    """
    user = CriarUsuario(**test_dados_usuarios)
    db_user = criar_usuario(db=db, usuario=user)

    assert db_user is not None
    assert db_user.nome_usuario == test_dados_usuarios["nome_usuario"]
    assert db_user.email_usuario == test_dados_usuarios["email_usuario"]
    assert db_user.senha != test_dados_usuarios["senha"]
    assert ModeloUsuario.verificar_senha(test_dados_usuarios["senha"], db_user.senha)


def test_registrar_usuario_via_api(cliente: TestClient, db: Session, test_dados_usuarios):
    """
    Teste para registrar um usuário via API
    """
    response = cliente.post("/usuario/registrar", json=test_dados_usuarios)

    assert response.status_code == 200
    data = response.json()
    assert data["nome_usuario"] == test_dados_usuarios["nome_usuario"]
    assert data["email_usuario"] == test_dados_usuarios["email_usuario"]
    assert "usuario_id" in data
    assert "senha" not in data


def test_registrar_usuario_email_duplicado(cliente: TestClient, db: Session, test_dados_usuarios):
    """
    Teste para verificar duplicidade de email no registro
    """
    
    response = cliente.post("/usuario/registrar", json=test_dados_usuarios)
    assert response.status_code == 200

    response = cliente.post("/usuario/registrar", json=test_dados_usuarios)
    assert response.status_code == 400
    assert "Email já cadastrado" in response.json()["detail"]


def test_login_usuario(cliente: TestClient, db: Session, test_dados_usuarios):
    """
    Teste de login do usuário
    """
    # Primeiro registra um usuário
    cliente.post("/usuario/registrar", json=test_dados_usuarios)

    # Tenta fazer login
    login_data = {
        "username": test_dados_usuarios["email_usuario"],
        "password": test_dados_usuarios["senha"],
    }

    response = cliente.post("/auth/login", data=login_data)

    assert response.status_code == 200
    data = response.json()
    assert "token_acesso" in data
    assert "token_refresh" in data


def test_login_usuario_credenciais_invalidas(cliente: TestClient, db: Session, test_dados_usuarios):
    """
    Teste de login com credenciais inválidas
    """
    cliente.post("/usuario/registrar", json=test_dados_usuarios)

    login_data = {
        "username": test_dados_usuarios["email_usuario"],
        "password": "senha_errada",
    }

    response = cliente.post("/auth/login", data=login_data)

    assert response.status_code == 401
    assert "Senha incorreta" in response.json()["detail"]

def test_token_invalido(cliente, test_dados_usuarios):
    """
    Teste que rejeita tokens inválidos
    """
    
    usuario_id, _ = _criar_usuario_obter_token(cliente, test_dados_usuarios)
    token_invalido = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0QGV4YW1wbGUuY29tIiwiZXhwIjoxNjE2MTUyMDAwfQ.invalid_signature"
    response = cliente.get(
        f"/usuario/{usuario_id}", headers={"Authorization": f"Bearer {token_invalido}"}
    )

    assert response.status_code == 401
    assert "Não foi possível validar as credenciais" in response.json()["detail"]