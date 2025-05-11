import difflib


def encontrar_resposta(
    pergunta_usuario: str, base_respostas: dict, nome_usuario: str = None
) -> str:
    """
    Função responsável por encontrar a resposta mais similar à pergunta do usuário.
    """
    pergunta_usuario = pergunta_usuario.strip().lower()
    pergunta_similar = difflib.get_close_matches(
        pergunta_usuario, base_respostas.keys(), n=1, cutoff=0.6
    )

    if pergunta_similar:
        resposta = base_respostas[pergunta_similar[0]]
        if nome_usuario and "{nome}" in resposta:
            resposta = resposta.format(nome=nome_usuario)
        return resposta
    return "Desculpe, não entendi a pergunta."


respostas = {
    "olá": "Olá, {nome}! Como posso ajudar você?",
    "qual o seu nome?": "Sou o Carteirito, um chatbot da Iplan Rio.",
    "pode verificar meu saldo?": (
        "Claro, {nome}! Você pode perguntar 'Qual o saldo do VT?'"
    ),
    "meu vt serve em quais transportes?": (
        "Seu cartão pode ser usado para pagar por viagens de ônibus, metrô ou trem. "
        "O valor será automaticamente descontado do seu saldo."
    ),
    "tchau": "Até logo, {nome}!",
}
