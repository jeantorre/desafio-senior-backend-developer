import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


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



