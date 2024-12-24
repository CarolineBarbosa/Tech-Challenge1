import requests
from bs4 import BeautifulSoup

#Faz o scraping dos dados de produção, processamento e comercialização do site da Embrapa.
def scraper_dados(aba):
    if(aba == "producao"):
        url = "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_02"
    elif(aba == "processamento"):
        url = "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_03"
    elif(aba == "comercializacao"):
        url = "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_04"
    elif(aba == "importacao"):
        url = "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_05"
    elif(aba == "exportacao"):
        url = "hhttp://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_06"
        
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception(f"Erro ao acessar os dados: {response.status_code}")
    
    soup = BeautifulSoup(response.text, "html.parser")
    table = table = soup.find("table", {"class": "tb_base tb_dados"})  # Localiza a tabela desejada
    data = []
    
    # Iterar sobre as linhas da tabela (exceto cabeçalhos)
    for row in table.find_all("tr")[1:]:
        cols = row.find_all("td")
        data.append({
            "Produto": cols[0].text.strip(),
            "Quantidade": None if (cols[1].text.strip() == "-") else (int(cols[1].text.strip().replace(".", ""))) # Converter para número
        })
    
    return data

def scraper_dados_impo_expor(aba):
    if(aba == "importacao"):
        url = "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_05"
    elif(aba == "exportacao"):
        url = "hhttp://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_06"
        
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception(f"Erro ao acessar os dados: {response.status_code}")
    
    soup = BeautifulSoup(response.text, "html.parser")
    table = table = soup.find("table", {"class": "tb_base tb_dados"})  # Localiza a tabela desejada
    data = []
    
    # Iterar sobre as linhas da tabela (exceto cabeçalhos)
    for row in table.find_all("tr")[1:]:
        cols = row.find_all("td")
        data.append({
            "País": cols[0].text.strip(),
            "Quantidade": None if (cols[1].text.strip() == "-") else (int(cols[1].text.strip().replace(".", ""))),
            "Valor": None if (cols[2].text.strip() == "-") else (int(cols[2].text.strip().replace(".", "")))
        })
    
    return data