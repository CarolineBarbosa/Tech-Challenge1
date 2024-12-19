from fastapi import APIRouter

router = APIRouter()

@router.get("/Produção", tags=["Produção"])
async def get_productions():
    return 1

@router.get("Processamento", tags=["Processamento"])
async def get_productions():
    return 1

@router.get("Comercialização", tags=["Comercialização"])
async def get_productions():
    return 1

@router.get("Importação", tags=["Importação"])
async def get_productions():
    return 1

@router.get("Exportação", tags=["Exportação"])
async def get_productions():
    return 1