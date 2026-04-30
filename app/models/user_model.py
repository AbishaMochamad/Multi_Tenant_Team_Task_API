from typing import Annotated
from pydantic import ConfigDict, StringConstraints, EmailStr, SecretStr, BaseModel, Field

from app.models.commons import Audit, Token


class CreateUserModel(BaseModel):
    first_name: Annotated[str, StringConstraints(max_length=50)]
    last_name: Annotated[str, StringConstraints(max_length=50)]
    email: Annotated[EmailStr, StringConstraints(max_length=50)]
    password: SecretStr = Field(exclude=True)


class UserModel(CreateUserModel, Audit):
    model_config = ConfigDict(from_attributes=True)

    id: int


class UserModelWithAccessToken(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    user: UserModel
    token: Token
