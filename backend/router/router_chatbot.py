from chat.chatbot import encontrar_resposta, respostas
from database import get_db
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from utils.auth import get_usuario_atual, verificar_bearer_token

router_chatbot = APIRouter(
    prefix="/chatbot",
    responses={404: {"descricao": "Não encontrado"}},
    tags=["Chatbot"],
)


class Pergunta(BaseModel):
    pergunta: str


@router_chatbot.post(
    "/",
    summary="Carteirinha Chatbot",
    description="Chatbot para interação com o usuário.",
    dependencies=[Depends(get_usuario_atual), Depends(verificar_bearer_token)],
)
async def chatbot(
    pergunta: Pergunta,
    usuario_atual=Depends(get_usuario_atual),
    db: Session = Depends(get_db),
):
    query = pergunta.pergunta.strip().lower()
    nome_usuario = usuario_atual.nome_usuario.title()
    if "saldo" in query and ("vale transporte" in query or "vt" in query):
        try:
            from router.router_transacao import get_saldo_vale_transporte

            resultado = await get_saldo_vale_transporte(
                id_usuario=usuario_atual.usuario_id, db=db
            )
            return {
                "resposta": (
                    f"{nome_usuario}, seu saldo atual é de "
                    f"R$ {resultado['saldo']:.2f}"
                )
            }
        except HTTPException as e:
            if e.status_code == 404:
                return {
                    "resposta": (
                        "Não foi possível encontrar informações sobre "
                        "seu vale transporte."
                    )
                }
            return {
                "resposta": (
                    "Ocorreu um erro ao consultar seu saldo. "
                    "Por favor, tente novamente mais tarde."
                )
            }

    return {"resposta": encontrar_resposta(pergunta.pergunta, respostas, nome_usuario)}
