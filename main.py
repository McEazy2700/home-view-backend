import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter
from core.schema import schema

allowed_origins = [
    "http://localhost:3000"
]

app = FastAPI()
graphql_app = GraphQLRouter(schema=schema)
app.include_router(graphql_app, prefix="/graphql")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


if __name__ == "__main__":
    uvicorn.run(app)
