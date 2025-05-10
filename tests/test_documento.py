from .test_auth import _criar_usuario_obter_token


def test_criar_documento(cliente, test_dados_usuarios, test_dados_documento):
    """
    Testes para criar um documento
    """

    _, token = _criar_usuario_obter_token(cliente, test_dados_usuarios)

    response = cliente.post(
        "/documento/registrar",
        json=test_dados_documento,
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["descricao_documento"] == test_dados_documento["descricao_documento"]
    assert data["sigla_documento"] == test_dados_documento["sigla_documento"]
