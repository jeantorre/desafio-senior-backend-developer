from fastapi import APIRouter

router_teste_backend = APIRouter(
    prefix="/health",
    responses={404: {"description": "Não encontrado"}},
    tags=["Health"],
    include_in_schema=False,
)


@router_teste_backend.get(
    "/", description="Verifica se o backend está funcionando", status_code=200
)
async def get_health():
    return {"Mensagem": "Backend está funcionando"}
