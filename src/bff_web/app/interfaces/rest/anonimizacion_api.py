from fastapi import APIRouter, HTTPException, status, Depends
from app.infrastructure.gateways import anonimizacion_gateway
from app.infrastructure.gateways import solicitudes_gateway
from app.infrastructure.gateways import registro_gateway
from app.infrastructure.security.token_validator import verify_token

router = APIRouter()

@router.get("/anonimizacion/{id}")
async def get_anonimizacion_state(id: str, token: str = Depends(verify_token)):
    try:
        state = anonimizacion_gateway.get_anonimizacion_state(id)
        return {"state": state}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/solicitudes/{username}")
async def get_anonimizacion_list(username: str, token: str = Depends(verify_token)):
    try:
        state = solicitudes_gateway.get_all_solicitudes(username)
        return {"state": state}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/registro")
async def create_registro(data: dict):
    try:
        result = registro_gateway.create_registro(data)
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
