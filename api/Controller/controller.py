from fastapi import APIRouter, Depends, Query
from Service import scraper, service
from utils.auth_util import get_current_user
from typing import Optional



router = APIRouter(
    dependencies=[Depends(get_current_user)]  # Aplica a validação JWT em todas as rotas
)

subOptProces = {"Viníferas": "01", "Americanas e híbridas": "02", "Uvas de mesa": "03" , "Sem classificação": "04"}
subImpExp = {"Vinhos de mesa": "01", "Espumantes": "02", "Uvas frescas": "03" , "Uvas passas": "04", "Suco de uva": "05"}

@router.get("/")
def home():
    return "Hello Anonimous user!"