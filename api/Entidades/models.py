from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Access(Base):
    __tablename__ = 'Access'
    id = Column(Integer, primary_key=True, autoincrement=True)
    User = Column(String, nullable=False)
    Hashed_password = Column(String, nullable=False)

class Producao(Base):
    """
    Representa a tabela 'Producai' no banco de dados.

    Atributos:
        id (Integer): Chave primária da tabela.
        produto (String): Nome do produto.
        Quantidade_Litros (Integer): Quantidade do produto.
        Ano (Integer): Ano relacionado aos produtos.
    """
    __tablename__ = 'Producao'
    id = Column(Integer, primary_key=True)
    Produto = Column(String)
    Quantidade = Column(Integer)
    Ano = Column(Integer)

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
    produto = Column(String)
    quantidade = Column(Integer)
    ano = Column(Integer)
    segmento = Column(String)

class Comercializacao(Base):
    """
    Representa a tabela 'Comercializacao' no banco de dados.

    Atributos:
        id (Integer): Chave primária da tabela.
        Produto (String): Nome do produto.
        Quantidade (Integer): Quantidade do produto.
        Ano (Integer): Ano relacionado ao registro.
    """
    __tablename__ = 'Comercializacao'
    id = Column(Integer, primary_key=True, autoincrement=True)
    Produto = Column(String(300))
    Quantidade = Column(Integer)
    Ano = Column(Integer)


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
    __tablename__ = 'Processamento'
    id = Column(Integer, primary_key=True)
    Cultivar = Column(String)
    Quantidade_Kg = Column(Integer)
    Ano = Column(Integer)
    Classificacao = Column(String)

class Exportacao(Base):
    """
    Representa a tabela 'Exportacao' no banco de dados.

    Atributos:
        id (Integer): Chave primária da tabela.
        Países (String): País referente a exportação.
        Quantidade (Integer): Quantidade  em Kg.
        Valor: Quantidade gasta de dinheiro.
        Tipos (String): Se é vinhos de mesa, espumantes, uvas frescas, suco de uva.
        Ano (Integer): Ano relacionado ao registro.
    """
    __tablename__ = 'Exportacao'
    id = Column(Integer, primary_key=True)
    País= Column(String)
    Quantidade_Kg = Column(Integer)
    Valor = Column(Integer)
    Tipos = Column(String)
    Ano = Column(Integer)

class Importacao(Base):
    """
    Representa a tabela 'Importacao' no banco de dados.

    Atributos:
        id (Integer): Chave primária da tabela.
        Países (String): País referente a exportação.
        Quantidade (Integer): Quantidade  em Kg.
        Valor: Quantidade gasta de dinheiro.
        Tipos (String): Se é vinhos de mesa, espumantes, uvas frescas, suco de uva.
        Ano (Integer): Ano relacionado ao registro.
    """
    __tablename__ = 'Importacao'
    id = Column(Integer, primary_key=True)
    País= Column(String)
    Quantidade_Kg = Column(Integer)
    Valor = Column(Integer)
    Tipos = Column(String)
    Ano = Column(Integer)

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