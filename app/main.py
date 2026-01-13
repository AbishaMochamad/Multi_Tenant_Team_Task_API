from fastapi import FastAPI
from .routers import users_router

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


app.include_router(users_router)
