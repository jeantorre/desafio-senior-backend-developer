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


def validador_numero(valor):
    """
    Valida se o valor é uma string e se contém apenas dígitos.

    param: valor - valor a ser validado
    return: valor após validação
    """
    if valor is None:
        return valor
    if not isinstance(valor, str):
        raise ValueError("Número precisa ser uma string")
    if not valor.isdigit():
        raise ValueError("Número precisa conter apenas dígitos")
    return valor
