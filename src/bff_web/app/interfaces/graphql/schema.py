import strawberry
from typing import Optional
from app.infrastructure.gateways import auth_gateway, anonimizacion_gateway

@strawberry.scalar(description="Scalar para datos JSON")
class JSON:
    @staticmethod
    def serialize(value: Any) -> Any:
        return value

    @staticmethod
    def parse_value(value: Any) -> Any:
        return value

@strawberry.type
class Query:
    @strawberry.field
    def validate_token(self, token: str) -> bool:
        return auth_gateway.validate_jwt(token)

    @strawberry.field
    def anonimizacion_state(self, id: str) -> Optional[JSON]:
        try:
            return anonimizacion_gateway.get_anonimizacion_state(id)
        except Exception:
            return None

schema = strawberry.Schema(query=Query)
