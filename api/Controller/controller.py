from fastapi import APIRouter, Depends, Query
from api.Service import scraper, service
from api.utils.auth_util import get_current_user
from typing import Optional


router = APIRouter(
     dependencies=[Depends(get_current_user)]  # Aplica a validação JWT em todas as rotas
)

subOptProces = {"Viníferas": "01", "Americanas e híbridas": "02", "Uvas de mesa": "03" , "Sem classificação": "04"}
subImpExp = {"Vinhos de mesa": "01", "Espumantes": "02", "Uvas frescas": "03" , "Uvas passas": "04", "Suco de uva": "05"}

@router.get("/Producao", tags=["Producao"])
async def get_producao(ano : int = Query(None,enum= [year for year in reversed(range(1970, 2024))])):
    return scraper.get_scraper("02", ano)

@router.post("/Producao", tags=["Producao"])
async def post_producao(ano : int = Query(None,enum= [year for year in reversed(range(1970, 2024))])):
    return service.insert_producao("02", ano)

@router.get("/Processamento", tags=["Processamento"])
async def get_processamento(ano : int = Query(None,enum= [year for year in reversed(range(1970, 2024))]), subopt: Optional[str] = Query(None, enum=["Viníferas", "Americanas e híbridas", "Uvas de mesa", "Sem classificação"])):
    return scraper.get_scraper("03", ano, subOptProces.get(subopt), subopt)

@router.post("/Processamento", tags=["Processamento"])
async def post_processamento(ano : int = Query(None,enum= [year for year in reversed(range(1970, 2024))]), subopt: Optional[str] = Query(None, enum=["Viníferas", "Americanas e híbridas", "Uvas de mesa", "Sem classificação"])):
    return service.insert_processamento("03", ano, subOptProces.get(subopt), subopt)

@router.get("/Comercializacao", tags=["Comercializacao"])
async def get_comercializacao(ano : int = Query(None,enum= [year for year in reversed(range(1970, 2024))])):
    return scraper.get_scraper("04", ano)

@router.post("/ComercializacaoInserir", tags=["Comercializacao"])
async def post_comercializacao(ano : int = Query(None,enum= [year for year in reversed(range(1970, 2024))])):
    return service.insert_comercializacao("04", ano)

@router.get("/Importacao", tags=["Importacao"])
async def get_importacao(ano : int = Query(None,enum= [year for year in reversed(range(1970, 2024))]), subopt: Optional[str] = Query(None, enum=["Vinhos de mesa", "Espumantes", "Uvas frescas", "Uvas passas", "Suco de uva"])):
    return scraper.get_scraper("05", ano, subImpExp.get(subopt))

@router.post("/ImportacaoInserir", tags=["Importacao"])
async def post_importacao(ano : int = Query(None,enum= [year for year in reversed(range(1970, 2024))]), subopt: Optional[str] = Query(None, enum=["Vinhos de mesa", "Espumantes", "Uvas frescas", "Uvas passas", "Suco de uva"])):
    return service.insert_importacao("05",ano, subImpExp.get(subopt), subopt)

@router.get("/Exportacao", tags=["Exportacao"])
async def get_exportacao(ano : int = Query(None,enum= [year for year in reversed(range(1970, 2024))]), subopt: Optional[str] = Query(None, enum=["Vinhos de mesa", "Espumantes", "Uvas frescas", "Uvas passas", "Suco de uva"])):
    return scraper.get_scraper("06", ano, subImpExp.get(subopt), subopt)

@router.post("/ExportacaoInserir", tags=["Exportacao"])
async def post_exportacao(ano : int = Query(None,enum= [year for year in reversed(range(1970, 2024))]), subopt: Optional[str] = Query(None, enum=["Vinhos de mesa", "Espumantes", "Uvas frescas", "Uvas passas", "Suco de uva"])):
    return service.insert_exportacao("06",ano, subImpExp.get(subopt), subopt)
