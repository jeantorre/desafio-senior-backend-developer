from database import SessionLocal, engine
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from router import router_auth, router_usuario
from utils.init_db import reset_db

load_dotenv()

reset_db(engine)
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


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router_auth)
app.include_router(router_usuario)
