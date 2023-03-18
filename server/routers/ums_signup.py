from fastapi import APIRouter, Header, HTTPException, status
from ..models import user
from ..utils import exceptions

router = APIRouter(prefix="/api/ums")

# signup
@router.post("/signup")
async def signup(user: user.NewUserModel):
    return user


# login
@router.post("/signin")
async def signup(user: user.ExistingUserModel):
    return user


# tokentest
@router.post("/test", status_code=status.HTTP_201_CREATED)
async def token(token: str | None = Header(default=None)):
    if not token:
        raise exceptions.getUserException()
    return token
