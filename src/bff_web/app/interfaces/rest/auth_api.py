from fastapi import APIRouter, HTTPException, status
from app.infrastructure.gateways import auth_gateway

router = APIRouter()

@router.post("/auth")
async def authenticate(token: str):
    if not auth_gateway.validate_jwt(token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
    return {"message": "Token válido"}
