import os

from database import SessionLocal, engine
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from router import (
    router_auth,
    router_chatbot,
    router_documento,
    router_teste_backend,
    router_transacao,
    router_transporte,
    router_usuario,
)
from utils import init_prod_db, reset_db

environment = os.getenv("ENVIRONMENT", "dev")
load_dotenv(f".env.{environment}")

if os.getenv("ENVIRONMENT") == "dev":
    reset_db(engine)
    db = SessionLocal()
    db.close()
else:
    init_prod_db(engine)
    db = SessionLocal()
    db.close()

app = FastAPI(
    title="Desafio Técnico - Desenvolvedor Backend Sênior - Iplan Rio",
    description=("API para gerenciamento da Carteira Digital"),
    version="1.0.0",
    contact={
        "name": "Jean Torre",
    },
    license_info={
        "name": "Prefeitura Rio - Iplan",
    },
    openapi_tags=[
        {
            "name": "Autenticação",
            "description": "Gerenciamento de autenticação de usuários",
        },
        {
            "name": "Usuários",
            "description": "Gerenciamento de usuários",
        },
        {
            "name": "Documentos",
            "description": "Gerenciamento de documentos",
        },
        {
            "name": "Transportes",
            "description": "Gerenciamento de transportes",
        },
        {
            "name": "Transações",
            "description": "Gerenciamento de transações",
        },
        {
            "name": "Chatbot",
            "description": "Chatbot para interação com o usuário",
        },
    ],
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    error_details = exc.errors()
    error_message = []
    for error in error_details:
        error_message.append(
            f"{error['msg']} at {' -> '.join(str(x) for x in error['loc'])}"
        )
    raise HTTPException(status_code=422, detail=error_details)


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):

    if isinstance(exc, HTTPException):

        if not isinstance(exc.detail, (str, list, dict, int, float, bool, type(None))):
            exc.detail = str(exc.detail)
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)},
    )


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router_auth)
app.include_router(router_usuario)
app.include_router(router_documento)
app.include_router(router_transporte)
app.include_router(router_transacao)
app.include_router(router_teste_backend)
app.include_router(router_chatbot)
