from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from utils.auth_util import authenticate_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()

@router.post("/auth/login", tags=["Authentication"], include_in_schema=False)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Endpoint para autenticação do usuário.
    """
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas"
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
