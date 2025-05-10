import pytest
from crud import atualizar_usuario, criar_usuario, deletar_usuario, ler_usuario
from fastapi.testclient import TestClient
from schema import AtualizarUsuario, CriarUsuario
from sqlalchemy.orm import Session


def _create_user_and_get_token(client, test_user_data):
    """Helper to create user and get auth token"""
    # Register user
    response = client.post("/usuario/registrar", json=test_user_data)
    user_id = response.json()["usuario_id"]

    # Login to get token
    login_data = {
        "username": test_user_data["email_usuario"],
        "password": test_user_data["senha"],
    }

    response = client.post("/auth/login", data=login_data)
    token = response.json()["token_acesso"]

    return user_id, token


def test_ler_usuarios(client: TestClient, test_user_data):
    """Test listing all users"""
    # Create user and get auth token
    user_id, token = _create_user_and_get_token(client, test_user_data)

    # Get all users
    response = client.get("/usuario/", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    users = response.json()
    assert len(users) >= 1
    assert any(user["usuario_id"] == user_id for user in users)


def test_ler_usuario_por_id(client: TestClient, test_user_data):
    """Test getting a single user by ID"""
    # Create user and get auth token
    user_id, token = _create_user_and_get_token(client, test_user_data)

    # Get user by ID
    response = client.get(
        f"/usuario/{user_id}", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    user = response.json()
    assert user["usuario_id"] == user_id
    assert user["nome_usuario"] == test_user_data["nome_usuario"]
    assert user["email_usuario"] == test_user_data["email_usuario"]


def test_ler_usuario_inexistente(client: TestClient, test_user_data):
    """Test getting a non-existent user"""
    # Create user and get auth token
    _, token = _create_user_and_get_token(client, test_user_data)

    # Try to get non-existent user
    response = client.get(
        "/usuario/non-existent-id", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404
    assert "Usuário não encontrado" in response.json()["detail"]


def test_atualizar_usuario_senha(client: TestClient, test_user_data):
    """Test updating user password"""
    # Create user and get auth token
    user_id, token = _create_user_and_get_token(client, test_user_data)

    # Update user password
    update_data = {
        "senha_atual": test_user_data["senha"],
        "nova_senha": "new_password123",
    }

    response = client.put(
        f"/usuario/{user_id}",
        json=update_data,
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200

    # Try to login with new password
    login_data = {
        "username": test_user_data["email_usuario"],
        "password": "new_password123",
    }

    response = client.post("/auth/login", data=login_data)
    assert response.status_code == 200
    assert "token_acesso" in response.json()


def test_atualizar_usuario_senha_incorreta(client: TestClient, test_user_data):
    """Test updating user password with incorrect current password"""
    # Create user and get auth token
    user_id, token = _create_user_and_get_token(client, test_user_data)

    # Try to update with incorrect password
    update_data = {"senha_atual": "wrong_password", "nova_senha": "new_password123"}

    response = client.put(
        f"/usuario/{user_id}",
        json=update_data,
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 400
    assert "Senha atual incorreta" in response.json()["detail"]


def test_deletar_usuario(client: TestClient, test_user_data):
    """Test deleting a user"""
    # Create user and get auth token
    user_id, token = _create_user_and_get_token(client, test_user_data)

    # Delete user
    response = client.delete(
        f"/usuario/{user_id}", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200

    # Try to get deleted user
    response = client.get(
        f"/usuario/{user_id}", headers={"Authorization": f"Bearer {token}"}
    )

    # This could fail with 401 if token validation depends on user existence
    # or could return 404 if not - both are acceptable depending on implementation
    assert response.status_code in (401, 404)
