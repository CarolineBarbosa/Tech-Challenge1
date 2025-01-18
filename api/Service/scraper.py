import requests
from bs4 import BeautifulSoup
from typing import Optional
from api.database.db_connector import *
from sqlalchemy import and_
from sqlalchemy.orm import Session
from api.Entidades.render_backup import get_table_name,get_columns,display_data

# Função para acessar a url com limite de tentativa pré definido de 200

def processa_request(url, max_tentativa_acesso = 2000):

  i = 1
  while i < max_tentativa_acesso:

    try:
      data = requests.get(url).text

      print("Acesso OK para url na iteração nº", i)
      i = max_tentativa_acesso + 1
    except:
    #   print("Erro listar_subsegmento")
        i += 1
        return None

  return data


def get_scraper(opcao: str, ano: Optional[str] = None ,subopt: Optional[str] = 1, subop: Optional[str] = None):
    url = f"http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao=opt_{opcao}&subopcao=subopt_{subopt}"
    data = processa_request(url)
    if data is None:        # se o request falhar em todas as tentativas, resgatamos os dados do backup

        return handle_backup_data(opcao, ano, subopt)
    else:
        if ano is None:
            df_full = []
            for year in reversed(range(1970, 2024)):
                df_full.append(scraper_dados(data, opcao, year, subop))
            return df_full
        else:
            return scraper_dados(data, opcao, ano, subopt, subop)


#Faz o scraping dos dados de produção, processamento e comercialização do site da Embrapa.
def scraper_dados(data, opcao: str, ano: Optional[str] = None ,subopt: Optional[str] = 1, subop: Optional[str] = None):
    
    # url = f"http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao=opt_{opcao}&subopcao=subopt_{subopt}"
    
    # soup = BeautifulSoup(processa_request(url), "html.parser")
    soup = BeautifulSoup(data, "html.parser")
    table = table = soup.find("table", {"class": "tb_base tb_dados"})  # Localiza a tabela desejada
    data = []
    
    if(opcao == "02" or opcao == "04"):
       # Iterar sobre as linhas da tabela (exceto cabeçalhos)
        for row in table.find_all("tr")[1:]:
            cols = row.find_all("td")
            data.append({
                "Produto": cols[0].text.strip(),
                "Quantidade": None if (cols[1].text.strip() == "-" or cols[1].text.strip() == "nd") else (int(cols[1].text.strip().replace(".", ""))), # Converter para número
                "Ano": ano
            })
    elif(opcao =="03"):
        # Iterar sobre as linhas da tabela (exceto cabeçalhos)
        for row in table.find_all("tr")[1:]:
            cols = row.find_all("td")
            data.append({
                "Cultivar": cols[0].text.strip(),
                "Quantidade_Kg": None if (cols[1].text.strip() == "-" or cols[1].text.strip() == "nd") else (int(cols[1].text.strip().replace(".", ""))), # Converter para número
                "Classificacao": subop,
                "Ano": ano
            })
    elif(opcao == "05" or opcao == "06"):
        # Iterar sobre as linhas da tabela (exceto cabeçalhos)
        for row in table.find_all("tr")[1:]:
            cols = row.find_all("td")
            data.append({
                "País": cols[0].text.strip(),
                "Quantidade_Kg": None if (cols[1].text.strip() == "-" or cols[1].text.strip() == "nd") else (int(cols[1].text.strip().replace(".", ""))),
                "Valor": None if (cols[2].text.strip() == "-" or cols[1].text.strip() == "nd") else (int(cols[2].text.strip().replace(".", ""))),
                "Tipos": subop,
                "Ano": ano
            })
    
    return data

def handle_backup_data(opcao, ano, subopt=None):
    db_manager = DatabaseManager()
    table_name = get_table_name(opcao) 
    columns, fixed_columns = get_columns(opcao, ano)
    query = f"SELECT {columns} FROM  {table_name}"
    backup_data = db_manager.read_from_database(query)
    
    if opcao in ["02", "03", "04"]:
        backup_data.columns = [col.lower() for col in backup_data.columns]
        df_long = backup_data.melt(id_vars=fixed_columns, var_name="Ano", value_name="Quantidade")
    
    elif opcao in ["05", "06"]:
        quantidade_cols = [col for col in backup_data.columns if "Quantidade" in col]
        quantidade_long = backup_data.melt(id_vars='País', value_vars=quantidade_cols, 
                                            var_name="Ano", value_name="Quantidade")
        quantidade_long["Ano"] = quantidade_long["Ano"].str.extract(r"(\d{4})")
        
        valor_cols = [col for col in backup_data.columns if "Valor" in col]
        valor_long = backup_data.melt(id_vars='País', value_vars=valor_cols, 
                                        var_name="Ano", value_name="Valor")
        valor_long["Ano"] = valor_long["Ano"].str.extract(r"(\d{4})")
        
        df_long = pd.merge(quantidade_long, valor_long, on=['País', "Ano"])
    print(subopt)
    if opcao in ['03', '05', '06'] and subopt !="01" :
        print('entrou')
        return "Erro ao conectar no site da Embrapa! Dados de backup não disponíveis para a subopção selecionada"
    else:
        print(df_long)
        return display_data(df_long, opcao)
