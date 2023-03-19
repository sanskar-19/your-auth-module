from pydantic import BaseModel, EmailStr
from ..utils import user as Utiluser


class NewUser(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str


class ExistingUser(BaseModel):
    email: EmailStr
    password: str


class NewUserInDb(BaseModel):
    uid: str
    first_name: str
    last_name: str
    email: EmailStr
    hashed_password: str
    role: str | None = "admin"
