import requests
from bs4 import BeautifulSoup
from typing import Optional

#Faz o scraping dos dados de produção, processamento e comercialização do site da Embrapa.
def scraper_dados(opcao: str, ano: Optional[str] = None ,subopt: Optional[str] = 1):
    
    url = f"http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao=opt_{opcao}&subopcao=subopt_{subopt}"
        
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception(f"Erro ao acessar os dados: {response.status_code}")
    
    soup = BeautifulSoup(response.text, "html.parser")
    table = table = soup.find("table", {"class": "tb_base tb_dados"})  # Localiza a tabela desejada
    data = []
    
    if(opcao == "02" or opcao == "03" or opcao == "04"):
        # Iterar sobre as linhas da tabela (exceto cabeçalhos)
        for row in table.find_all("tr")[1:]:
            cols = row.find_all("td")
            data.append({
                "Produto": cols[0].text.strip(),
                "Quantidade": None if (cols[1].text.strip() == "-") else (int(cols[1].text.strip().replace(".", ""))) # Converter para número
            })
    elif(opcao == "05" or opcao == "06"):
        # Iterar sobre as linhas da tabela (exceto cabeçalhos)
        for row in table.find_all("tr")[1:]:
            cols = row.find_all("td")
            data.append({
                "País": cols[0].text.strip(),
                "Quantidade": None if (cols[1].text.strip() == "-") else (int(cols[1].text.strip().replace(".", ""))),
                "Valor": None if (cols[2].text.strip() == "-") else (int(cols[2].text.strip().replace(".", "")))
            })
    
    return data