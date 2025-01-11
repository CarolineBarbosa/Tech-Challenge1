from db_connector import *
from sqlalchemy import and_

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
db_url_sqlite = "sqlite:///tech_challenge.db"  
db_manager = DatabaseManager(db_url_sqlite)

# Cria as tabelas
db_manager.create_tables()

# Insere dados de exemplo
db_manager.insert_from_dataframe(Quantidade, df_quantidade)

# Leitura dos dados
filters = [and_(Quantidade.ano == 2023, Quantidade.segmento == "Produção")]

df_filtered = db_manager.read_to_dataframe(Quantidade, filters=filters)

df_filtered