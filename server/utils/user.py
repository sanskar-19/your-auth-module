from ..schema import user as user_schema
from datetime import datetime
import uuid
from passlib.context import CryptContext
from ..models import user

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Create new user for the db
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
    new_user = user_schema.NewUserInDb(
        uid=str(uid),
        first_name=first_name,
        last_name=last_name,
        email=email,
        hashed_password=generate_hash(password),
        role=role,
        created_at=datetime.now(),
    )

    return user.UserModel(**new_user.dict())


def verify_password(password: str, hashed_password: str):
    return pwd_context.verify(password, hashed_password)


def generate_hash(password: str):
    return pwd_context.hash(password)
