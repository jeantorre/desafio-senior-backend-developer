import os
import secrets

from dotenv import load_dotenv, set_key


def criar_secret_key():
    """
    Gera e salva uma secret key para funcionamento da aplicação, caso ela ainda não tenha
    sido criada.
    """
    environment = os.getenv("ENVIRONMENT", "dev")
    dotenv_path = os.path.join(os.getcwd(), f".env.{environment}")

    if not os.path.isfile(dotenv_path):
        print(f"Arquivo {dotenv_path} não encontrado.")
        return

    load_dotenv(dotenv_path)

    if not os.getenv("SECRET_KEY"):
        secret_key = secrets.token_hex(32)

        set_key(dotenv_path, "SECRET_KEY", secret_key)
        print(f"Secret Key gerada e salva em {dotenv_path}")
    else:
        print("Secret Key já existe")


criar_secret_key()
