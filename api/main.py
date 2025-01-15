from fastapi import FastAPI
from api.Controller import controller, auth
from api.utils import auth_util

app = FastAPI()

# Rotas de produção
app.include_router(controller.router)

# Rotas de autenticação

app.include_router(auth.router)