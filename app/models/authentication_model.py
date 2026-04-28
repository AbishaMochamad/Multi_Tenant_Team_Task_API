from pydantic import BaseModel, EmailStr, Field,  SecretStr, StringConstraints, model_validator
from typing import Annotated
from typing_extensions import Self

from app.models.commons.audit import Audit
from app.models.user_model import CreateUserModel


class LoginRequest(BaseModel):
    email: Annotated[EmailStr, StringConstraints(max_length=50)]
    password: SecretStr

class RegisterRequest(CreateUserModel, Audit):
    confirm_password: SecretStr = Field(exclude=True)
    
    @model_validator(mode="after")
    def check_passwords_match(self) -> Self:
        if self.password != self.confirm_password:
            raise ValueError("Password do not Match")
        return self
