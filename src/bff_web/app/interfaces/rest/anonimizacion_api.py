from fastapi import APIRouter, HTTPException, status, Depends
from app.infrastructure.gateways import anonimizacion_gateway
from app.infrastructure.security.token_validator import verify_token

router = APIRouter()

@router.get("/anonimizacion/{id}")
async def get_anonimizacion_state(id: str, token: str = Depends(verify_token)):
    try:
        state = anonimizacion_gateway.get_anonimizacion_state(id)
        return {"state": state}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
