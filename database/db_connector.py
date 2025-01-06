import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker


Base = declarative_base()


class Quantidade(Base):
    """
    Representa a tabela 'quantidade' no banco de dados.

    Atributos:
        id (Integer): Chave primária da tabela.
        produto (String): Nome do produto.
        quantidade (Integer): Quantidade do produto.
        ano (Integer): Ano relacionado ao registro.
        segmento (String): Segmento (Produção, Comercialização, etc.).
    """
    __tablename__ = 'quantidade'
    id = Column(Integer, primary_key=True)
    produto = Column(String, nullable=False)
    quantidade = Column(Integer, nullable=False)
    ano = Column(Integer, nullable=False)
    segmento = Column(String, nullable=False)


class Processamento(Base):
    """
    Representa a tabela 'processamento' no banco de dados.

    Atributos:
        id (Integer): Chave primária da tabela.
        cultivar (String): Tipo de cultivar processado.
        quantidade (Integer): Quantidade processada.
        ano (Integer): Ano relacionado ao registro.
        classificacao (String): Classificação do processamento.
    """
    __tablename__ = 'processamento'
    id = Column(Integer, primary_key=True)
    cultivar = Column(String, nullable=False)
    quantidade = Column(Integer, nullable=False)
    ano = Column(Integer, nullable=False)
    classificacao = Column(String, nullable=False)


class TipoComercio(Base):
    """
    Representa a tabela 'tipocomercio' no banco de dados.

    Atributos:
        id (Integer): Chave primária da tabela.
        paises (String): Países envolvidos no comércio.
        quantidade (Integer): Quantidade comercializada.
        valor (Float): Valor comercializado.
        tipo (String): Tipo de comércio (Exportação ou Importação).
        ano (Integer): Ano relacionado ao registro.
        derivados (String): Produtos derivados (opcional).
    """
    __tablename__ = 'tipocomercio'
    id = Column(Integer, primary_key=True)
    paises = Column(String, nullable=False)
    quantidade = Column(Integer, nullable=False)
    valor = Column(Float, nullable=False)
    tipo = Column(String, nullable=False)  # Exportação ou Importação
    ano = Column(Integer, nullable=False)
    derivados = Column(String, nullable=True)


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
    def __init__(self, db_url):
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
