from pydantic import BaseModel


class NewUserModel(BaseModel):
    name: str
    email: str
    password: str


class ExistingUserModel(BaseModel):
    email: str
    password: str
