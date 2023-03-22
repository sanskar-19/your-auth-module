from fastapi import APIRouter, Header, status, Depends, HTTPException
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
)
async def signup(user: user_schema.NewUser, db: Session = Depends(get_db)):

    # Creating new user
    try:
        return add_new_user_to_db(db, user.dict())
    except Exception as e:
        raise e


@router.get(
    "/fetch-user-details",
    status_code=status.HTTP_200_OK,
    response_model=user_schema.UserDetails,
)
async def get_user_details(token: str = Header(), db: Session = Depends(get_db)):
    try:
        return fetch_user_from_db(db, token)
    except Exception as e:
        raise e


# create login route
# @router.post(
#     "/login",
#     response_model=user_schema.ResponseModel,
# )
# async def login(user: user_schema.ExistingUser):
#     for db_user in db.users:
#         if db_user["email"] == user.email:
#             if user_utils.verify_password(
#                 password=user.password, hashed_password=db_user["hashed_password"]
#             ):
#                 token = jwt_utils.create_access_token(
#                     uid=db_user["uid"], email=db_user["email"], role=db_user["role"]
#                 )
#                 return {
#                     "data": {
#                         "token": token,
#                     },
#                     "message": "User logged in successfully",
#                 }

#             else:
#                 raise exceptions.e_invalid_credentials()
#     raise exceptions.e_user_not_found()


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


#######################################################################################################################################
def fetch_user_from_db(db: Session, token: str):
    try:
        payload = jwt_utils.validate_access_token(access_token=token)
        email = payload["email"]
        user = db.query(UserModel).filter(UserModel.email == email).first()

        # If no user exists
        if user is None:
            raise exceptions.e_user_not_found()
        else:
            return user

    # Handling exceptions from JWT failure
    except Exception as e:
        raise (e)


#######################################################################################################################################
def add_new_user_to_db(db: Session, user: dict):
    try:
        user_from_db = (
            db.query(UserModel).filter(UserModel.email == user["email"]).first()
        )

        if user_from_db is not None:
            raise exceptions.e_user_already_exists()
        else:
            user_in_db = user_utils.create_new_user(**user)
            db.add(user_in_db)
            db.commit()

            token = jwt_utils.create_access_token(
                uid=user_in_db.uid, email=user_in_db.email, role=user_in_db.role
            )
            return {
                "data": {
                    "access_token": token,
                },
                "message": "User added successfully",
            }
    except Exception as e:
        if e is HTTPException:
            raise e
        else:
            raise e
