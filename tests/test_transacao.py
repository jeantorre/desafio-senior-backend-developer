from crud import associar_vale_transporte
from sqlalchemy.orm import Session

from .test_auth import _criar_usuario_obter_token


def test_criar_transacao(
    cliente, db: Session, test_dados_transacao, test_dados_usuarios
):
    """
    Teste para realizar uma transação.
    """
    usuario_id, token = _criar_usuario_obter_token(cliente, test_dados_usuarios)

    associar_vale_transporte(db=db, usuario_id=usuario_id)

    response = cliente.post(
        f"/transacao/criar_transacao_vt/{usuario_id}",
        params={
            "tipo_transacao": test_dados_transacao["tipo_transacao"],
            "valor_transacao": test_dados_transacao["valor_transacao"],
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    data = response.json()
    assert "transacao_id" in data
    assert float(data["valor_transacao"]) == test_dados_transacao["valor_transacao"]


def test_verificar_saldo_apos_transacao(
    cliente, db: Session, test_dados_transacao, test_dados_usuarios
):
    """
    Teste para verificar o saldo após uma transação.
    """

    usuario_id, token = _criar_usuario_obter_token(cliente, test_dados_usuarios)
    associar_vale_transporte(db=db, usuario_id=usuario_id)

    response = cliente.post(
        f"/transacao/criar_transacao_vt/{usuario_id}",
        params={
            "tipo_transacao": test_dados_transacao["tipo_transacao"],
            "valor_transacao": test_dados_transacao["valor_transacao"],
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    dados_recarga = response.json()
    saldo_inicial = dados_recarga["valor_transacao"]

    response = cliente.post(
        f"/transacao/criar_transacao_vt/{usuario_id}",
        params={"tipo_transacao": 2, "tipo_transporte": 1, "valor_transacao": 1},
        headers={"Authorization": f"Bearer {token}"},
    )

    valor_gasto = response.json()["valor_transacao"]

    assert float(saldo_inicial) - float(valor_gasto) == 44.5
