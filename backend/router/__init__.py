from .router_auth import router_auth
from .router_documento import router_documento
from .router_test_backend import router_teste_backend
from .router_transacao import router_transacao
from .router_transporte import router_transporte
from .router_usuario import router_usuario

__all__ = [
    "router_auth",
    "router_usuario",
    "router_documento",
    "router_transporte",
    "router_transacao",
    "router_teste_backend",
]
