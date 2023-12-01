import re
from typing import Annotated, Optional

from pydantic import BaseModel, computed_field, EmailStr, PositiveInt, Field


class User(BaseModel):
    name: str
    age: Optional[PositiveInt] = Field(default=None, gt=0, lt=100)


class UserAgeResponse(User):
    @computed_field(return_type=bool)
    @property
    def is_adult(self):
        return self.age >= 18


class UserCreate(User):
    email: EmailStr
    is_subscribed: bool = False
