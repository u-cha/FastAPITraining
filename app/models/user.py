from pydantic import BaseModel, computed_field


class User(BaseModel):
    name: str
    age: int


class UserAgeResponse(User):
    @computed_field(return_type=bool)
    @property
    def is_adult(self):
        return self.age >= 18
