from fastapi import APIRouter, Header, status
from ..models import user as user_models
from ..utils import db, exceptions, jwt as jwt_utils, user as user_utils


router = APIRouter(prefix="/api/ums")

# signup
@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(user: user_models.NewUser):

    # Creating new user
    new_user = user_utils.create_new_user(**user.dict())

    # Check if user already exists in a db
    flag = False
    for db_user in db.users:
        if db_user["email"] == user.email:
            flag = True
            break

    if flag:
        raise exceptions.e_user_already_exists()

    else:
        db.users.append(new_user)

    return {
        "users": db.users,
        "message": "user added successfully",
        "token": jwt_utils.create_access_token(
            uid=new_user["uid"], email=user.email, role="admin"
        ),
    }


# validate-token
@router.post("/validate-token")
async def validate_token(token: str = Header()):
    try:
        payload = jwt_utils.validate_access_token(access_token=token)
        return payload
    except Exception as e:
        raise e


# validate-password
@router.post("/validate-password")
async def check_password(password: str, hashed_password: str):
    if user_utils.verify_password(password=password, hashed_password=hashed_password):
        return "Password Verified"
    else:
        raise exceptions.e_invalid_credentials()


# create login route
@router.post("/login")
async def login(user: user_models.ExistingUser):
    for db_user in db.users:
        if db_user["email"] == user.email:
            if user_utils.verify_password(
                password=user.password, hashed_password=db_user["hashed_password"]
            ):
                token = jwt_utils.create_access_token(
                    uid=db_user["uid"], email=db_user["email"], role="admin"
                )
                return {"token": token, "message": "Token created successfully"}
            else:
                raise exceptions.e_invalid_credentials()
    raise exceptions.e_user_not_found()
