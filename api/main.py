from fastapi import FastAPI
from Controller import controller, auth
from utils import auth_util

app = FastAPI()

# Rotas de produção
app.include_router(controller.router)
