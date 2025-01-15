import requests
from bs4 import BeautifulSoup
from typing import Optional
from database.db_connector import *
from sqlalchemy import and_
from sqlalchemy.orm import Session

# Função para acessar a url com limite de tentativa pré definido de 200

def processa_request(url, max_tentativa_acesso = 2000):

  i = 1
  while i < max_tentativa_acesso:

    try:
      data = requests.get(url).text

      print("Acesso OK para url na iteração nº", i)
      i = max_tentativa_acesso + 1
    except:
      print("Erro listar_subsegmento")
      data = get_data_from_db()
      i += 1
  return data

# Função para obter dados do banco de dados
def get_data_from_db():
    with open('Scripts/InsertBackupComercio.sql', 'r') as file:
        data = file.read()
    return data

def get_scraper(opcao: str, ano: Optional[str] = None ,subopt: Optional[str] = 1, subop: Optional[str] = None):
    if ano is None:
        df_full = []
        for year in reversed(range(1970, 2024)):
            df_full.append(scraper_dados(opcao, year, subopt, subop))
        return df_full
    else:
        return scraper_dados(opcao, ano, subopt, subop)


#Faz o scraping dos dados de produção, processamento e comercialização do site da Embrapa.
def scraper_dados(opcao: str, ano: Optional[str] = None ,subopt: Optional[str] = 1, subop: Optional[str] = None):
    
    url = f"http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao=opt_{opcao}&subopcao=subopt_{subopt}"
    
    soup = BeautifulSoup(processa_request(url), "html.parser")
    table = table = soup.find("table", {"class": "tb_base tb_dados"})  # Localiza a tabela desejada
    data = []
    
    if(opcao == "02" or opcao == "04"):
        # Iterar sobre as linhas da tabela (exceto cabeçalhos)
        for row in table.find_all("tr")[1:]:
            cols = row.find_all("td")
            data.append({
                "Produto": cols[0].text.strip(),
                "Quantidade": None if (cols[1].text.strip() == "-") else (int(cols[1].text.strip().replace(".", ""))), # Converter para número
                "Ano": ano
            })
    elif(opcao =="03"):
        # Iterar sobre as linhas da tabela (exceto cabeçalhos)
        for row in table.find_all("tr")[1:]:
            cols = row.find_all("td")
            data.append({
                "Cultivar": cols[0].text.strip(),
                "Quantidade_Kg": None if (cols[1].text.strip() == "-") else (int(cols[1].text.strip().replace(".", ""))), # Converter para número
                "Classificacao": subop,
                "Ano": ano
            })
    elif(opcao == "05" or opcao == "06"):
        # Iterar sobre as linhas da tabela (exceto cabeçalhos)
        for row in table.find_all("tr")[1:]:
            cols = row.find_all("td")
            data.append({
                "País": cols[0].text.strip(),
                "Quantidade_Kg": None if (cols[1].text.strip() == "-") else (int(cols[1].text.strip().replace(".", ""))),
                "Valor": None if (cols[2].text.strip() == "-") else (int(cols[2].text.strip().replace(".", ""))),
                "Tipos": subop,
                "Ano": ano
            })
    
    return data