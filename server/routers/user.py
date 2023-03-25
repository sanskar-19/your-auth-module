from fastapi import APIRouter, Header, status, Depends, HTTPException
from ..schema import user as user_schema
from ..utils import db, exceptions, jwt as jwt_utils, user as user_utils
from ..models.user import UserModel
from sqlalchemy.orm import Session
from ..database import get_db
from pydantic import EmailStr
from datetime import datetime, timedelta

db = get_db()

router = APIRouter(prefix="/api/ums")

# Signup as a new user
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


# Login
@router.post(
    "/login", response_model=user_schema.ResponseModel, status_code=status.HTTP_200_OK
)
async def login(user: user_schema.ExistingUser, db: Session = Depends(get_db)):
    try:
        user_from_db = db.query(UserModel).filter(UserModel.email == user.email).first()
        if user_from_db is None:
            raise exceptions.e_user_not_found()
        else:
            if user_utils.verify_password(
                password=user.password, hashed_password=user_from_db.hashed_password
            ):
                token = jwt_utils.create_access_token(
                    uid=user_from_db.uid,
                    email=user_from_db.email,
                    role=user_from_db.role,
                )
                return {
                    "data": {"access_token": token},
                    "message": "Logged in successfully",
                }
            else:
                raise exceptions.e_invalid_credentials()

    except Exception as e:
        raise e


# Fetch user details from token
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


# reset password using otp
@router.post(
    "/reset-password",
    response_model=user_schema.ResponseModel,
)
async def reset_password(
    new_password: user_schema.ResetPassword, db: Session = Depends(get_db)
):
    try:
        user_from_db = db.query(UserModel).filter(UserModel.email == new_password.email)
        if user_from_db is None:
            raise exceptions.e_user_not_found()

        otp, otp_expiry = user_from_db.first().otp, user_from_db.first().otp_expiry_at

        if otp is None:
            raise exceptions.e_generate_otp_first()

        if datetime.now() > otp_expiry:
            raise exceptions.e_otp_expired()

        if otp == new_password.otp:
            user_from_db.update(
                {
                    UserModel.hashed_password: user_utils.generate_hash(
                        new_password.new_password
                    ),
                    UserModel.otp: None,
                    UserModel.otp_expiry_at: None,
                }
            )
            db.commit()
            return {"data": {}, "message": "Password Reset Successfully"}
        else:
            raise exceptions.e_otp_mistmached()
    except Exception as e:
        raise e


# send password reset email
@router.post(
    "/send-password-reset-email",
    response_model=user_schema.ResponseModel,
)
async def send_password_reset_email(email: EmailStr, db: Session = Depends(get_db)):
    try:
        user_from_db = db.query(UserModel).filter(UserModel.email == email)
        if user_from_db.first() is None:
            raise exceptions.e_user_not_found()

        last_otp_expiry = user_from_db.first().otp_expiry_at
        if last_otp_expiry is not None and last_otp_expiry > datetime.now():
            raise exceptions.e_otp_not_expired(
                wait_time=(last_otp_expiry - datetime.now()).seconds
            )
        else:
            otp, otp_expiry_at = user_utils.generate_otp()
            user_from_db.update(
                {UserModel.otp: otp, UserModel.otp_expiry_at: otp_expiry_at}
            )
            db.commit()
            return {
                "data": {
                    "otp": otp,
                    "validity": otp_expiry_at,
                },
                "message": "Otp generated successfully",
            }
    except Exception as e:
        raise e


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
