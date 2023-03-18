from pydantic import BaseModel , EmailStr
from ..utils import user as Utiluser

class NewUserModel(BaseModel):

    user_id:int
    first_name: str
    last_name: str
    last_name:str
    email: str
    password: str


class ExistingUserModel(BaseModel):
    email: str
    password: str



# class UserOut(BaseModel):
#     username: str
#     email: EmailStr
#     full_name: str | None = None


class UserInDB(BaseModel):
    user_id: int
    username: str
    key:bytes
    encoded_password: bytes
    email: EmailStr
    full_name: str | None = None

    def fake_save_user(new_user: NewUserModel):
        key,encoded_password = Utiluser.encode_password(NewUserModel.password)
        user_in_db = UserInDB(**new_user.dict(), key=key,encoded_password=encoded_password)
        print("User saved! ..not really")
        return user_in_db