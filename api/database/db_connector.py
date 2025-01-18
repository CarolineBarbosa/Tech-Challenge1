import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Float, text
from sqlalchemy.orm import declarative_base, sessionmaker
from typing import Optional
from api.Entidades.models import Base


class DatabaseManager:
    """
    Gerencia as operações no banco de dados, incluindo a criação de tabelas,
    inserção de dados a partir de DataFrames e leitura de dados para DataFrames.

    Métodos:
        __init__(db_url): Inicializa o gerenciador com a URL do banco de dados.
        create_tables(): Cria todas as tabelas definidas no modelo Base.
        insert_from_dataframe(table_class, dataframe): Insere dados no banco
            de dados a partir de um DataFrame.
        read_to_dataframe(table_class, filters): Lê dados do banco e os retorna
            como um DataFrame do Pandas.
    """
    def __init__(self, db_url: Optional[str] = "sqlite:///tech_challenge.db"):
        """
        Inicializa o DatabaseManager com a URL do banco de dados.

        Parâmetros:
            db_url (str): URL de conexão com o banco de dados.
        """
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)

    def create_tables(self):
        """
        Cria todas as tabelas definidas no modelo Base no banco de dados.
        """
        Base.metadata.create_all(self.engine)

    def insert_from_dataframe(self, table_class, dataframe):
        """
        Insere dados no banco de dados a partir de um DataFrame do Pandas.

        Parâmetros:
            table_class (Base): Classe ORM representando a tabela.
            dataframe (DataFrame): DataFrame contendo os dados a serem inseridos.
        """
        session = self.Session()
        
        try:
            records = dataframe.to_dict(orient='records')
            session.bulk_insert_mappings(table_class, records)
            session.commit()

        except Exception as e:
            session.rollback()
            print(f"Erro ao inserir dados: {e}")

        finally:
            session.close()

    def read_to_dataframe(self, table_class, filters=None):
        """
        Lê dados do banco de dados e os retorna como um DataFrame do Pandas.

        Parâmetros:
            table_class (Base): Classe ORM representando a tabela a ser consultada.
            filters (list, opcional): Condições de filtro SQLAlchemy para a consulta.

        Retorna:
            DataFrame: DataFrame do Pandas contendo os resultados da consulta.
        """
        session = self.Session()

        try:
            query = session.query(table_class)

            if filters:
                query = query.filter(*filters)

            result = pd.read_sql(query.statement, self.engine)
            return result
        
        except Exception as e:
            print(f"Erro ao ler dados: {e}")
            return pd.DataFrame()  # Retorna um DataFrame vazio em caso de erro
        
        finally:
            session.close()

    def read_from_database(self, query: str) -> pd.DataFrame:
        """
        Executa uma consulta SQL no banco de dados e retorna os resultados como um DataFrame do Pandas.

        Parâmetros:
            query (str): Consulta SQL a ser executada.

        Retorna:
            DataFrame: DataFrame do Pandas contendo os resultados da consulta.
        """
        with self.engine.connect() as connection:
            try:
                result = connection.execute(text(query))
                df = pd.DataFrame(result.fetchall(), columns=result.keys())
                return df
            except Exception as e:
                print(f"Erro ao executar consulta: {e}")
                return pd.DataFrame()


    def execute_script(self, script: str):
    #Executa um script SQL diretamente no banco de dados. Parâmetros: script (str): Script SQL a ser executado.
        with self.engine.connect() as connection:
            try:
                connection.execute(script)
                print("Script executado com sucesso.")
            except Exception as e:
                print(f"Erro ao executar script: {e}")

    def execute_select(self, script: str):
        with self.engine.connect() as connection:
            try:
                result = connection.execute(text(script))
                df = pd.DataFrame(result.fetchall(), columns=result.keys())
                return df
            except Exception as e:
                print(f"Erro ao executar script: {e}")
                return pd.DataFrame()
    
    def inserir_dados_quantidade(self, tabelaNome: str, id: int, produto: str, quantidade: int, ano: int, segmento: str):

        with self.engine.connect() as connection:
            try:
                result = connection.execute(text(script))
                df = pd.DataFrame(result.fetchall(), columns=result.keys())
                return df
            except Exception as e:
                print(f"Erro ao executar script: {e}")
                return pd.DataFrame()
            
    def inserir_dados_comercializacao(self, produto: str, quantidade: int, ano: int):
        script = f"INSERT INTO Comercialização(Produto, Quantidade, Ano) VALUES({id}, {produto}, {quantidade}, {ano})"
        with self.engine.connect() as connection:
            try:
                result = connection.execute(text(script))
                df = pd.DataFrame(result.fetchall(), columns=result.keys())
                return df
            except Exception as e:
                print(f"Erro ao executar script: {e}")
                return pd.DataFrame()
    def get_user(self, username: str, password: str):
        script = f"SELECT Hashed_password FROM Access WHERE User = {username}"
        with self.engine.connect() as connection:
            try:
                result = connection.execute(text(script))
                df = pd.DataFrame(result.fetchall(), columns=result.keys())
                if not df.empty:
                    return df.iloc[0]
                else:
                    return None
            except Exception as e:
                print(f"Erro ao executar script: {e}")
                return pd.DataFrame()