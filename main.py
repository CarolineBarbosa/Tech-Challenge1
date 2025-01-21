from fastapi import FastAPI
from api.Controller import controller, auth
from api.utils import auth_util

app = FastAPI()

# Rota Favicon para evitar 404 por /favicon.ico
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return {"message": "No favicon"}

# Rotas de produção
app.include_router(controller.router)

# Rotas de autenticação

app.include_router(auth.router)