import uvicorn
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from core.schema import schema


app = FastAPI()
graphql_app = GraphQLRouter(schema=schema)
app.include_router(graphql_app, prefix="/graphql")


if __name__ == "__main__":
    uvicorn.run(app)
