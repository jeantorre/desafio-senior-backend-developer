import re

import unidecode


def maiuscula_sem_acento(valor: str) -> str:
    """
    Remove a acentuação das strings e as deixa
    em maiúscula.

    param: valor - string a ser formatada
    return: string após formatação
    """
    if isinstance(valor, str):
        valor = unidecode.unidecode(valor)
        valor = re.sub(r"[^a-zA-Z0-9\s,]", "", valor)
        return valor.upper()
    return valor
