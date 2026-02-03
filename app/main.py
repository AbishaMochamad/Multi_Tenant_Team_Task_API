from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from .api import users_router
from datetime import datetime, timezone
from sqlalchemy.exc import IntegrityError, OperationalError


app = FastAPI()


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "detail": "An expected error occured",
            "path": request.url.path,
            "timestamp": str(datetime.now(timezone.utc)),
        },
    )


@app.exception_handler(IntegrityError)
async def integrity_error_handler(request, exc):
    return JSONResponse(status_code=500, content={"detail": str(exc.orig)})


@app.exception_handler(OperationalError)
async def database_error_handler(request, exc):
    return JSONResponse(status_code=500, content={"detail": str(exc.orig)})


@app.get("/")
def read_root():
    return {"Hello": "World"}


app.include_router(users_router)
