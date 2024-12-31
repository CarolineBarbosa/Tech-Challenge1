from fastapi import APIRouter, Depends
import Service.Scraper as scraper
from utils.auth_util import get_current_user


router = APIRouter(
    dependencies=[Depends(get_current_user)]  # Aplica a validação JWT em todas as rotas
)



@router.get("/Produção", tags=["Produção"])
async def get_producao():
    scraper.scraper_dados("producao")
    return 1

@router.get("/Processamento", tags=["Processamento"])
async def get_processamento():
    scraper.scraper_dados("processamento")
    return 1
@router.get("/Comercialização", tags=["Comercialização"])
async def get_comercializacao():
    scraper.scraper_dados("comercializacao")
    return 1

@router.get("/Importação", tags=["Importação"])
async def get_importacao():
    scraper.scraper_dados_impo_expor("importacao")
    return 1

@router.get("/Exportação", tags=["Exportação"])
async def get_exportacao():
    scraper.scraper_dados_impo_expor("exportacao")
    return 1
