import jwt
import time
from datetime import datetime, timedelta
from cryptography.hazmat.primitives import serialization


def load_private_key(pk_file_path: str, password: str | None = ""):
    f = open(pk_file_path, "r")
    private_key = f.read()
    f.close()
    return serialization.load_ssh_private_key(
        private_key.encode(), password=bytes(password.encode())
    )


def load_public_key(pk_file_path: str):
    f = open(pk_file_path, "r")
    public_key = f.read()
    f.close()
    return serialization.load_ssh_public_key(public_key.encode())

pu = load_public_key(pk_file_path='server\\utils\\keys\\id_rsa.pub')
pr = load_private_key(pk_file_path='server\\utils\\keys\\id_rsa')

pu = load_public_key(pk_file_path="server\\utils\\keys\\id_rsa.pub")
pr = load_private_key(pk_file_path="server\\utils\\keys\\id_rsa")


def create_access_token(userid: str, email: str, role: str | None):
    payload = {
        "uid": userid,
        "email": email,
        "role": role,
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(seconds=30),
    }
    return jwt.encode(payload, key=pr, algorithm="RS256")


def validate_access_token(access_token: str):
    try:
        payload = jwt.decode(access_token, key=pu, algorithms="RS256")

        if payload["exp"] <= time.time():
            raise ExpiredTokenError("Token Expired")

        return payload

    except Exception as e:
        raise e


class ExpiredTokenError(Exception):
    def __init__(self, msg):
        Exception(msg)
