from fastapi import APIRouter, HTTPException, status
from app.infrastructure.gateways import registro_gateway

router = APIRouter()

@router.post("/registro")
async def create_registro(data: dict):
    try:
        result = registro_gateway.create_registro(data)
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
