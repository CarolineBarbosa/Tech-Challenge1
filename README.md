# Tech-Challenge1

Este repositório contém um projeto de exemplo utilizando FastAPI, uma framework moderna e rápida para construção de APIs com Python. O objetivo deste projeto é coletar dados de um website e armazená-los em um banco de dados. 

### Funcionalidades do Projeto

- **Coleta de Dados:** Utiliza a biblioteca `requests` para fazer requisições HTTP e a `beautifulsoup4` para fazer o parsing do HTML e extrair os dados necessários.
- **API RESTful:** Implementa uma API RESTful com FastAPI, permitindo a interação com os dados coletados através de endpoints definidos.
- **Segurança:** Inclui configuração básica de segurança utilizando a biblioteca `security` do FastAPI.
- **Modelos de Dados:** Define modelos de dados utilizando Pydantic para validação e serialização dos dados.

### Estrutura do Projeto

O projeto está organizado da seguinte forma:

```
Tech-Challenge1/
├── api/
│   ├── main.py
│   ├── api/
│   │   ├── database/
│   │   │   └── crud.py
│   │   │   └── db_connector.py
│   │   └── Controller/
│   │   │   └── auth.py
│   │   │   └── controller.py
│   │   ├── Entidades/
│   │   │   └── models.py
│   │   │   └── render_backup.py
│   │   ├── Scripts/
│   │   │   └── sql-files
│   │   ├── Service/
│   │   │   └── service.py
│   │   │   └── scrapper.py
│   │   ├── utils/
│   │   │   └── auth_util.py
├── README.md
├── requirements.txt
└── .gitignore
```

### Instalação

Para instalar as dependências do projeto, execute:

```bash
pip install -r requirements.txt
```

### Executando a Aplicação

Para iniciar a aplicação, utilize o comando:

```bash
python -m uvicorn app.main:app --reload
```

A aplicação estará disponível em `http://127.0.0.1:8000/docs`.

### Diagrama do Projeto

<img width="904" alt="diagrama_api" src="https://github.com/user-attachments/assets/0cd50e81-ac3e-47cb-9dcc-6ba35291f0dc" />
