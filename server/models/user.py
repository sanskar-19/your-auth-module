from pydantic import BaseModel, EmailStr
from ..utils import user as Utiluser


class NewUserModel(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str


class ExistingUserModel(BaseModel):
    email: str
    password: str


# class UserOut(BaseModel):
#     username: str
#     email: EmailStr
#     full_name: str | None = None


class NewUserInDb(BaseModel):
    uid: str
    first_name: str
    last_name: str
    email: str
    hashed_password: str
    role: str | None = "admin"


class BaseUser(BaseModel):
    uid: str
    email: str
