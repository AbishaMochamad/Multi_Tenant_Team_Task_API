from pydantic import BaseModel


class ServerErrorResponse(BaseModel):
    detail: str
