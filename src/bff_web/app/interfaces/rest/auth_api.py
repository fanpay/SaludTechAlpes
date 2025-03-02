from fastapi import APIRouter, HTTPException, status
from app.infrastructure.gateways import auth_gateway
from app.config import API_KEYS
from app.infrastructure.security.token_validator import create_jwt
from datetime import datetime, timedelta

router = APIRouter()

@router.post("/auth/validate")
async def authenticate(token: str):
    if not auth_gateway.validate_jwt(token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
    return {"message": "Token válido"}


@router.post("/auth/authenticate")
async def authenticate(api_key: str):
    # Verificar si la API key existe en la configuración
    if api_key not in API_KEYS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key inválida"
        )

    # Extraer datos asociados a la API key
    user_data = API_KEYS[api_key]
    # Generar el JWT con la información del usuario
    token = create_jwt(payload={"sub": user_data["user"]}, expires_delta=timedelta(hours=1))
    return {"token": token, "user": user_data["user"]}
