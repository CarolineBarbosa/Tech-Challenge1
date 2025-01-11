
from typing import Optional
from database.db_connector import *
from sqlalchemy import and_
from Service import Scraper
import Entidades.models as model
from utils import auth_util


def insert_dados(palavra: str):
    # exemplo de dados
    data_quantidade = {
        "produto": ["Produto A", "Produto B"],
        "quantidade": [100, 200],
        "ano": [2023, 2024],
        "segmento": ["Produção", "Comercialização"]
    }
    df_quantidade = pd.DataFrame(data_quantidade)

    df_quantidade.head(3)

    # Inicializa o banco de dados 
    db_manager = DatabaseManager()

    # Cria as tabelas
    db_manager.create_tables()

    # Insere dados de exemplo
    db_manager.insert_from_dataframe(model.Quantidade, df_quantidade)

    # Leitura dos dados
    filters = [and_(model.Quantidade.ano == 2023, model.Quantidade.segmento == "Produção")]

    df_filtered = db_manager.read_to_dataframe(model.Quantidade, filters=filters)

    #df_filtered

    print(db_manager.execute_select("select * from quantidade"))

#Faz o scraping dos dados de produção, processamento e comercialização do site da Embrapa.
def insert_dados_comercializacao(opcao: str, ano: int):
    dados = scraper.scraper_dados(opcao, ano)
    db_manager = DatabaseManager()
    data_comercializacao = pd.DataFrame(dados)

    db_manager.insert_from_dataframe(model.Comercializacao, data_comercializacao)
    print(db_manager.execute_select("select * from Comercializacao"))

def insert_dados_exportacao(opcao: str, ano: int, subopt: int, subop: str) -> str:
    if ano is None:
        for a in range(1970, 2024): 
            dados = model.scraper.scraper_dados(opcao, a, subopt, subop)
    else:
        dados = model.scraper.scraper_dados(opcao, ano, subopt, subop)

    data_exportacao = pd.DataFrame(dados)
    db_manager = DatabaseManager()
    filters = [and_(model.Exportacao.Ano == ano, model.Exportacao.Tipos == subop)]
    if db_manager.read_to_dataframe(model.Exportacao, filters).empty:
        db_manager.insert_from_dataframe(model.Exportacao, data_exportacao)
        return "Dados inseridos com sucessor."
    else:
        return "Já existem dados para esse ano e opção selecionada."

def insert_dados_importacao(opcao: str, ano: int, subopt: int, subop: str) -> str:
    dados = scraper.scraper_dados(opcao, ano, subopt, subop)
    data_importacao = pd.DataFrame(dados)
    db_manager = DatabaseManager()
    filters = [and_(model.Importacao.Ano == ano, model.Importacao.Tipos == subop)]
    if db_manager.read_to_dataframe(model.Importacao, filters).empty:
        db_manager.insert_from_dataframe(model.Importacao, data_importacao)
        return "Dados inseridos com sucessor."
    else:
        return "Já existem dados para esse ano e opção selecionada."
    
def insert_dados_processamento(opcao: str, ano: int, subopt: int, subop: str) -> str:
    dados = scraper.scraper_dados(opcao, ano, subopt, subop)
    data_importacao = pd.DataFrame(dados)
    db_manager = DatabaseManager()
    filters = [and_(model.Processamento.Ano == ano, model.Processamento.Classificacao == subop)]
    if db_manager.read_to_dataframe(model.Processamento, filters).empty:
        db_manager.insert_from_dataframe(model.Processamento, data_importacao)
        return "Dados inseridos com sucessor."
    else:
        return "Já existem dados para esse ano e opção selecionada."
        
def autenticar_usuario(username: str, password: str):
    data_autenticar ={
        "User": [username],
        "Hashed_password": [password]
    }
    data_autenticar = pd.DataFrame(data_autenticar)
    db_manager = DatabaseManager()
    filters = [(model.Access.User == username)]
    user = db_manager.read_to_dataframe(model.Access, filters)
    return user