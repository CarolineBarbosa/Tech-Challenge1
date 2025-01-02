from fastapi import APIRouter, Depends, Query
import Service.Scraper as scraper
from utils.auth_util import get_current_user
from typing import Optional



router = APIRouter(
    dependencies=[Depends(get_current_user)]  # Aplica a validação JWT em todas as rotas
)

subOptProces = {"Viníferas": "01", "Americanas e híbridas": "02", "Uvas de mesa": "03" , "Sem classificação": "04"}
subImpExp = {"Vinhos de mesa": "01", "Espumantes": "02", "Uvas frescas": "03" , "Uvas passas": "04", "Suco de uva": "05"}

@router.post("/Produção", tags=["Produção"])
async def get_producao(ano: int = Query(None, ge=1970, le=2023)):
    return scraper.scraper_dados("02", ano)

@router.post("/Processamento", tags=["Processamento"])
async def get_processamento(ano : int = Query(None, ge=1970, le=2023), subopt: Optional[str] = Query(None, enum=["Viníferas", "Americanas e híbridas", "Uvas de mesa", "Sem classificação"])):
    return scraper.scraper_dados("03", ano, subOptProces.get(subopt))

@router.post("/Comercialização", tags=["Comercialização"])
async def get_comercializacao(ano : int = Query(None, ge=1970, le=2023)):
    return scraper.scraper_dados("04", ano)

@router.post("/Importação", tags=["Importação"])
async def get_importacao(ano : int = Query(None, ge=1970, le=2023), subopt: Optional[str] = Query(None, enum=["Vinhos de mesa", "Espumantes", "Uvas frescas", "Uvas passas", "Suco de uva"])):
    return scraper.scraper_dados("05", ano, subImpExp.get(subopt))

@router.post("/Exportação", tags=["Exportação"])
async def get_exportacao(ano : int = Query(None, ge=1970, le=2023), subopt: Optional[str] = Query(None, enum=["Vinhos de mesa", "Espumantes", "Uvas frescas", "Uvas passas", "Suco de uva"])):
    return scraper.scraper_dados("06", ano, subImpExp.get(subopt))
