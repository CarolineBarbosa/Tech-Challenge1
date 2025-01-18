
from typing import Optional
from api.database.db_connector import *
from sqlalchemy import and_
from api.Service import scraper
import api.Entidades.models as model
from api.utils import auth_util


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


def insert_producao(opcao: str, ano: Optional[str] = None ,subopt: Optional[str] = 1, subop: Optional[str] = None):
    if ano is None:
        df_full = []
        for year in reversed(range(1970, 2024)):
            df_full.append(insert_dados_producao(opcao, year, subopt, subop))
        return df_full
    else:
        return insert_dados_producao(opcao, ano, subopt, subop)
    
def insert_comercializacao(opcao: str, ano: Optional[str] = None ,subopt: Optional[str] = 1, subop: Optional[str] = None):
    if ano is None:
        df_full = []
        for year in reversed(range(1970, 2024)):
            df_full.append(insert_dados_comercializacao(opcao, year, subopt, subop))
        return df_full
    else:
        return insert_dados_comercializacao(opcao, ano, subopt, subop)
    
def insert_processamento(opcao: str, ano: Optional[str] = None ,subopt: Optional[str] = 1, subop: Optional[str] = None):
    if ano is None:
        df_full = []
        for year in reversed(range(1970, 2024)):
            df_full.append(insert_dados_processamento(opcao, year, subopt, subop))
        return df_full
    else:
        return insert_dados_processamento(opcao, ano, subopt, subop)
    
    
def insert_exportacao(opcao: str, ano: Optional[str] = None ,subopt: Optional[str] = 1, subop: Optional[str] = None):
    if ano is None:
        df_full = []
        for year in reversed(range(1970, 2024)):
            df_full.append(insert_dados_exportacao(opcao, year, subopt, subop))
        return df_full
    else:
        return insert_dados_exportacao(opcao, ano, subopt, subop)
    
def insert_importacao(opcao: str, ano: Optional[str] = None ,subopt: Optional[str] = 1, subop: Optional[str] = None):
    if ano is None:
        df_full = []
        for year in reversed(range(1970, 2024)):
            df_full.append(insert_dados_importacao(opcao, year, subopt, subop))
        return df_full
    else:
        return insert_dados_importacao(opcao, ano, subopt, subop)


def insert_dados_exportacao(opcao: str, ano: int, subopt: int, subop: str) -> str:

    dados = scraper.get_scraper(opcao, ano, subopt, subop)
    data_exportacao = pd.DataFrame(dados)
    db_manager = DatabaseManager()
    filters = [and_(model.Exportacao.Ano == ano, model.Exportacao.Tipos == subop)]
    if db_manager.read_to_dataframe(model.Exportacao, filters).empty:
        db_manager.insert_from_dataframe(model.Exportacao, data_exportacao)
        return "Dados inseridos com sucessor."
    else:
        return "Já existem dados para esse ano e opção selecionada."

def insert_dados_importacao(opcao: str, ano: int, subopt: int, subop: str) -> str:
    dados = scraper.get_scraper(opcao, ano, subopt, subop)
    data_importacao = pd.DataFrame(dados)
    db_manager = DatabaseManager()
    filters = [and_(model.Importacao.Ano == ano, model.Importacao.Tipos == subop)]
    if db_manager.read_to_dataframe(model.Importacao, filters).empty:
        db_manager.insert_from_dataframe(model.Importacao, data_importacao)
        return "Dados inseridos com sucessor."
    else:
        return "Já existem dados para esse ano e opção selecionada."
    
def insert_dados_producao(opcao: str, ano: int, subopt: int, subop: str) -> str:
    dados = scraper.get_scraper(opcao, ano, subopt, subop)
    data_importacao = pd.DataFrame(dados)
    db_manager = DatabaseManager()
    filters = [model.Producao.Ano == ano]
    if db_manager.read_to_dataframe(model.Producao, filters).empty:
        db_manager.insert_from_dataframe(model.Producao, data_importacao)
        return "Dados inseridos com sucessor."
    else:
        return "Já existem dados para esse ano."

def insert_dados_comercializacao(opcao: str, ano: int, subopt: int, subop: str) -> str:
    dados = scraper.get_scraper(opcao, ano, subopt, subop)
    data_importacao = pd.DataFrame(dados)
    db_manager = DatabaseManager()
    filters = [model.Comercializacao.Ano == ano]
    if db_manager.read_to_dataframe(model.Comercializacao, filters).empty:
        db_manager.insert_from_dataframe(model.Comercializacao, data_importacao)
        return "Dados inseridos com sucessor."
    else:
        return "Já existem dados para esse ano."
    
def insert_dados_processamento(opcao: str, ano: int, subopt: int, subop: str) -> str:
    dados = scraper.get_scraper(opcao, ano, subopt, subop)
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