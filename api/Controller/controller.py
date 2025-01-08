from fastapi import APIRouter, Depends, Query
from Service import scraper, service
from utils.auth_util import get_current_user
from typing import Optional



router = APIRouter(
    dependencies=[Depends(get_current_user)]  # Aplica a validação JWT em todas as rotas
)

subOptProces = {"Viníferas": "01", "Americanas e híbridas": "02", "Uvas de mesa": "03" , "Sem classificação": "04"}
subImpExp = {"Vinhos de mesa": "01", "Espumantes": "02", "Uvas frescas": "03" , "Uvas passas": "04", "Suco de uva": "05"}

@router.get("/Produção", tags=["Produção"])
async def get_producao(ano : int = Query(None,enum= [year for year in range(1970, 2024)])):
    return scraper.scraper_dados("02", ano)

@router.get("/Processamento", tags=["Processamento"])
async def get_processamento(ano : int = Query(None,enum= [year for year in range(1970, 2024)]), subopt: Optional[str] = Query(None, enum=["Viníferas", "Americanas e híbridas", "Uvas de mesa", "Sem classificação"])):
    return scraper.scraper_dados("03", ano, subOptProces.get(subopt), subopt)

@router.post("/Processamento", tags=["Processamento"])
async def get_processamento(ano : int = Query(None,enum= [year for year in range(1970, 2024)]), subopt: Optional[str] = Query(None, enum=["Viníferas", "Americanas e híbridas", "Uvas de mesa", "Sem classificação"])):
    return service.insert_dados_processamento("03", ano, subOptProces.get(subopt), subopt)

@router.get("/Comercialização", tags=["Comercialização"])
async def get_comercializacao(ano : int = Query(None,enum= [year for year in range(1970, 2024)])):
    return scraper.scraper_dados("04", ano)

@router.post("/ComercializaçãoInserir", tags=["Comercialização"])
async def get_comercializacao(ano : int = Query(None,enum= [year for year in range(1970, 2024)])):
    return service.insert_dados_comercializacao("04", ano)

@router.get("/Importação", tags=["Importação"])
async def get_importacao(ano : int = Query(None,enum= [year for year in range(1970, 2024)]), subopt: Optional[str] = Query(None, enum=["Vinhos de mesa", "Espumantes", "Uvas frescas", "Uvas passas", "Suco de uva"])):
    return scraper.scraper_dados("05", ano, subImpExp.get(subopt))

@router.post("/ImportaçãoInserir", tags=["Importação"])
async def get_importacao(ano : int = Query(None,enum= [year for year in range(1970, 2024)]), subopt: Optional[str] = Query(None, enum=["Vinhos de mesa", "Espumantes", "Uvas frescas", "Uvas passas", "Suco de uva"])):
    return service.insert_dados_importacao("05",ano, subImpExp.get(subopt), subopt)

@router.get("/Exportação", tags=["Exportação"])
async def get_exportacao(ano : int = Query(None,enum= [year for year in range(1970, 2024)]), subopt: Optional[str] = Query(None, enum=["Vinhos de mesa", "Espumantes", "Uvas frescas", "Uvas passas", "Suco de uva"])):
    return scraper.scraper_dados("06", ano, subImpExp.get(subopt), subopt)

@router.post("/ExportaçãoInserir", tags=["Exportação"])
async def get_exportacao(ano : int = Query(None,enum= [year for year in range(1970, 2024)]), subopt: Optional[str] = Query(None, enum=["Vinhos de mesa", "Espumantes", "Uvas frescas", "Uvas passas", "Suco de uva"])):
    return service.insert_dados_exportacao("06",ano, subImpExp.get(subopt), subopt)

@router.post("/Teste", tags=["Teste"])
async def get_exportacao():
    return service.insert_dados("07")
