from fastapi import APIRouter, Header, status
from ..models import user
from ..utils import exceptions, user as Utiluser
from typing import Union
from ..utils import jwt as jwt_utils, db, user as user_utils


router = APIRouter(prefix="/api/ums")

# signup
@router.post("/signup")
async def signup(user: user.NewUserModel):
    key, encoded_user_password = Utiluser.encode_password(
        user.password
    )  # this key and encoded password will be stored in DB

    new_user = user_utils.create_new_user(**user.dict())

    # Check if user already exists in a db
    if new_user["email"] in db.users:
        return "User Already Exits"

    else:
        db.users.append(new_user)

    return {
        "users": db.users,
        "message": "user added successfully",
        "token": jwt_utils.create_access_token(
            userid="1234", email=user.email, role="admin"
        ),
    }


# login
@router.post("/signin")
async def signin(user: user.ExistingUserModel):
    # token = jwt.create_access_token()
    return user


# tokentest
@router.post("/test", status_code=status.HTTP_201_CREATED)
async def token(token: str | None = Header(default=None)):
    if not token:
        raise exceptions.getUserException()
    return token
