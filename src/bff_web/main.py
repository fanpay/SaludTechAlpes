from fastapi import FastAPI

from app.interfaces.rest import auth_api, anonimizacion_api, registro_api
#from strawberry.asgi import GraphQL
# from app.interfaces.graphql.schema import *
import uvicorn

app = FastAPI(title="BFF Gateway")

# # Rutas REST (por ejemplo, versión v1)
app.include_router(auth_api.router, prefix="/v1/rest")
app.include_router(anonimizacion_api.router, prefix="/v1/rest")
app.include_router(registro_api.router, prefix="/v1/rest")

# # Montaje de GraphQL con Strawberry
# graphql_app = GraphQL(schema)
# app.mount("/v1/graphql", graphql_app)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
