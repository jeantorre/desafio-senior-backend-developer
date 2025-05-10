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


def _create_transporte(client, token, test_transporte_data):
    """Helper to create transport"""
    response = client.post(
        "/transporte/",
        json=test_transporte_data,
        headers={"Authorization": f"Bearer {token}"},
    )
    return response.json()["transporte_id"]


@pytest.fixture
def setup_test_environment(client, test_user_data, test_transporte_data):
    """Setup test environment for transactions"""
    user_id, token = _create_user_and_get_token(client, test_user_data)
    transporte_id = _create_transporte(client, token, test_transporte_data)

    return {"user_id": user_id, "token": token, "transporte_id": transporte_id}


def test_criar_transacao(client, setup_test_environment, test_transacao_data):
    """Test creating a transaction"""
    # Get token and transport ID
    token = setup_test_environment["token"]
    transporte_id = setup_test_environment["transporte_id"]

    # Create transaction
    test_transacao_data["transporte_id"] = transporte_id
    response = client.post(
        "/transacao/",
        json=test_transacao_data,
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    data = response.json()
    assert "transacao_id" in data
    assert data["valor_transacao"] == test_transacao_data["valor_transacao"]
    assert data["transporte_id"] == transporte_id


def test_ler_transacoes(client, setup_test_environment, test_transacao_data):
    """Test listing all transactions"""
    # Get token and transport ID
    token = setup_test_environment["token"]
    transporte_id = setup_test_environment["transporte_id"]

    # Create a transaction first
    test_transacao_data["transporte_id"] = transporte_id
    client.post(
        "/transacao/",
        json=test_transacao_data,
        headers={"Authorization": f"Bearer {token}"},
    )

    # Get all transactions
    response = client.get("/transacao/", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    transactions = response.json()
    assert len(transactions) >= 1
    # Check our created transaction exists in the list
    assert any(
        transaction["valor_transacao"] == test_transacao_data["valor_transacao"]
        and transaction["transporte_id"] == transporte_id
        for transaction in transactions
    )


def test_ler_transacao_por_id(client, setup_test_environment, test_transacao_data):
    """Test getting a transaction by ID"""
    # Get token and transport ID
    token = setup_test_environment["token"]
    transporte_id = setup_test_environment["transporte_id"]

    # Create a transaction first
    test_transacao_data["transporte_id"] = transporte_id
    response = client.post(
        "/transacao/",
        json=test_transacao_data,
        headers={"Authorization": f"Bearer {token}"},
    )
    transacao_id = response.json()["transacao_id"]

    # Get transaction by ID
    response = client.get(
        f"/transacao/{transacao_id}", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    transaction = response.json()
    assert transaction["transacao_id"] == transacao_id
    assert transaction["valor_transacao"] == test_transacao_data["valor_transacao"]
    assert transaction["transporte_id"] == transporte_id


def test_ler_transacao_inexistente(client, setup_test_environment):
    """Test getting a non-existent transaction"""
    token = setup_test_environment["token"]

    response = client.get(
        "/transacao/non-existent-id", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404
    assert "Transação não encontrada" in response.json()["detail"]


def test_verificar_saldo_apos_transacao(
    client, setup_test_environment, test_transacao_data
):
    """Test that transport balance is updated after transaction"""
    # Get token and transport ID
    token = setup_test_environment["token"]
    transporte_id = setup_test_environment["transporte_id"]

    # Get initial balance
    response = client.get(
        f"/transporte/{transporte_id}", headers={"Authorization": f"Bearer {token}"}
    )
    initial_balance = response.json()["saldo"]

    # Create a transaction
    test_transacao_data["transporte_id"] = transporte_id
    client.post(
        "/transacao/",
        json=test_transacao_data,
        headers={"Authorization": f"Bearer {token}"},
    )

    # Get updated balance
    response = client.get(
        f"/transporte/{transporte_id}", headers={"Authorization": f"Bearer {token}"}
    )
    updated_balance = response.json()["saldo"]

    # Since we're spending money, balance should decrease
    assert updated_balance == initial_balance - test_transacao_data["valor_transacao"]
