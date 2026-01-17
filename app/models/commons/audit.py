from typing import Annotated
from pydantic import BaseModel, StringConstraints
from pydantic_extra_types.pendulum_dt import DateTime


class Audit(BaseModel):
    created_by: Annotated[str, StringConstraints(max_length=50)]
    created_at: DateTime
    updated_by: Annotated[str, StringConstraints(max_length=50)]
    updated_at: DateTime
