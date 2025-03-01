from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.infrastructure.gateways import auth_gateway
from datetime import datetime, timedelta
import jwt
from jwt import PyJWTError

SECRET_KEY = "URG%36!K4b0D3jeWUIhgRMcTTk8qi5ej"
ALGORITHM = "HS256"

security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    if not auth_gateway.validate_jwt(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )
    return token


def create_jwt(payload: dict, expires_delta: timedelta = None) -> str:
    data = payload.copy()
    if expires_delta:
        data["exp"] = datetime.utcnow() + expires_delta
    else:
        data["exp"] = datetime.utcnow() + timedelta(minutes=15)
    token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return token
