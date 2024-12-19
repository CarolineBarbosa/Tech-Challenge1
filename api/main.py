from fastapi import FastAPI
from Controller import controller

app = FastAPI()

# Rotas de produção
app.include_router(controller.router)