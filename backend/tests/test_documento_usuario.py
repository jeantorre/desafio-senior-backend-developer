import pytest
from fastapi.testclient import TestClient
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


def test_criar_documento(client, test_user_data, test_documento_data):
    """Test creating a document"""
    # Create user and get token
    user_id, token = _create_user_and_get_token(client, test_user_data)

    # Create document
    test_documento_data["usuario_id"] = user_id
    response = client.post(
        "/documento/",
        json=test_documento_data,
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    data = response.json()
    assert "documento_id" in data
    assert data["tipo_documento"] == test_documento_data["tipo_documento"]
    assert data["numero_documento"] == test_documento_data["numero_documento"]


def test_associar_documento_usuario(client, test_user_data, test_documento_data):
    """Test associating a document with a user"""
    # Create user and get token
    user_id, token = _create_user_and_get_token(client, test_user_data)

    # Create document
    test_documento_data["usuario_id"] = user_id
    response = client.post(
        "/documento/",
        json=test_documento_data,
        headers={"Authorization": f"Bearer {token}"},
    )
    documento_id = response.json()["documento_id"]

    # Get user's documents
    response = client.get(
        f"/usuario/{user_id}/documentos", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    documentos = response.json()
    assert len(documentos) >= 1
    assert any(doc["documento_id"] == documento_id for doc in documentos)


def test_ler_documentos_de_outro_usuario(client, test_user_data, test_documento_data):
    """Test that a user cannot read another user's documents"""
    # Create first user and document
    user1_id, token1 = _create_user_and_get_token(client, test_user_data)
    test_documento_data["usuario_id"] = user1_id
    client.post(
        "/documento/",
        json=test_documento_data,
        headers={"Authorization": f"Bearer {token1}"},
    )

    # Create second user
    user2_data = {
        "nome_usuario": "Second User",
        "email_usuario": "second@example.com",
        "senha": "password123",
    }
    user2_id, token2 = _create_user_and_get_token(client, user2_data)

    # Try to access first user's documents with second user's token
    response = client.get(
        f"/usuario/{user1_id}/documentos", headers={"Authorization": f"Bearer {token2}"}
    )

    # Depending on implementation, this should either be forbidden (403)
    # or return an empty list as a security measure
    if response.status_code == 403:
        assert "Não autorizado" in response.json()["detail"]
    else:
        assert response.status_code == 200
        assert len(response.json()) == 0


def test_token_invalido(client, test_user_data):
    """Test that invalid tokens are rejected"""
    # Create user
    user_id, _ = _create_user_and_get_token(client, test_user_data)

    # Try to access a protected endpoint with invalid token
    invalid_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0QGV4YW1wbGUuY29tIiwiZXhwIjoxNjE2MTUyMDAwfQ.invalid_signature"
    response = client.get(
        f"/usuario/{user_id}", headers={"Authorization": f"Bearer {invalid_token}"}
    )

    assert response.status_code == 401
    assert "Não foi possível validar as credenciais" in response.json()["detail"]


def test_token_expirado(client, test_user_data):
    """Test that expired tokens are rejected"""
    # This test is more complex as we'd need to create an expired token
    # For now we'll just test with a manually created expired token

    # Create user
    user_id, _ = _create_user_and_get_token(client, test_user_data)

    # Token with expiration in the past
    expired_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0QGV4YW1wbGUuY29tIiwiZXhwIjoxNjE2MTUyMDAwfQ.dummysignature"
    response = client.get(
        f"/usuario/{user_id}", headers={"Authorization": f"Bearer {expired_token}"}
    )

    assert response.status_code == 401
    assert "Não foi possível validar as credenciais" in response.json()["detail"]
