from cryptography.fernet import Fernet
from ..models import user as user_models
import uuid
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(password: str, hashed_password: str):
    return pwd_context.verify(password, hashed_password)


def generate_hash(password: str):
    return pwd_context.hash(password)


def create_new_user(
    first_name: str,
    last_name: str,
    email: str,
    password: str,
    role: str | None = "admin",
):
    # Generate new uuid here
    uid = uuid.uuid4()

    # Create new user object for the db
    new_user = user_models.NewUserInDb(
        uid=str(uid),
        first_name=first_name,
        last_name=last_name,
        email=email,
        hashed_password=generate_hash(password),
        role=role,
    )

    return new_user.dict()
