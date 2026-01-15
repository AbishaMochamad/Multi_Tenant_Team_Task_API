from typing import Annotated
from pydantic import BaseModel, ConfigDict, StringConstraints, EmailStr
from pydantic_extra_types.pendulum_dt import DateTime


class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    first_name: Annotated[str, StringConstraints(max_length=50)]
    last_name: Annotated[str, StringConstraints(max_length=50)]
    email: Annotated[EmailStr, StringConstraints(max_length=50)]
    created_by: Annotated[str, StringConstraints(max_length=50)]
    created_at: DateTime
    updated_by: Annotated[str, StringConstraints(max_length=50)]
    updated_at: DateTime
