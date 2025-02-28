from fastapi import APIRouter, HTTPException, status
from app.infrastructure.gateways import anonimizacion_gateway

router = APIRouter()

@router.get("/anonimizacion/{id}")
async def get_anonimizacion_state(id: str):
    try:
        state = anonimizacion_gateway.get_anonimizacion_state(id)
        return {"state": state}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
