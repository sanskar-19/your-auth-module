from fastapi import APIRouter, Header, status, Depends
from ..schema import user as user_schema
from ..utils import db, exceptions, jwt as jwt_utils, user as user_utils
from ..models.user import UserModel
from sqlalchemy.orm import Session
from ..database import get_db

db = get_db()

router = APIRouter(prefix="/api/ums")

# signup
@router.post(
    "/signup",
    status_code=status.HTTP_201_CREATED,
    response_model=user_schema.ResponseModel,
)
async def signup(user: user_schema.NewUser, db: Session = Depends(get_db)):

    # Creating new user
    new_user = user_utils.create_new_user(**user.dict())
    print(new_user)
    db_user = UserModel(**new_user)
    db.add(db_user)
    db.commit()

    return {
        "data": {
            "users": new_user,
        },
        "message": "User added successfully",
    }


# create login route
@router.post(
    "/login",
    response_model=user_schema.ResponseModel,
)
async def login(user: user_schema.ExistingUser):
    for db_user in db.users:
        if db_user["email"] == user.email:
            if user_utils.verify_password(
                password=user.password, hashed_password=db_user["hashed_password"]
            ):
                token = jwt_utils.create_access_token(
                    uid=db_user["uid"], email=db_user["email"], role=db_user["role"]
                )
                return {
                    "data": {
                        "token": token,
                    },
                    "message": "User logged in successfully",
                }

            else:
                raise exceptions.e_invalid_credentials()
    raise exceptions.e_user_not_found()


# validate-token
@router.post(
    "/validate-token",
    response_model=user_schema.ResponseModel,
)
async def validate_token(token: str = Header()):
    try:
        payload = jwt_utils.validate_access_token(access_token=token)
        return {"data": payload, "message": "Token Validated"}
    except Exception as e:
        raise e
