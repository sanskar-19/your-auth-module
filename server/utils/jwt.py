import jwt
from cryptography.hazmat.primitives import serialization

# pu = load_public_key(pk_file_path=PUBLIC_KEY)
# pr = load_private_key(pk_file_path=PRIVATE_KEY)


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


def create_access_token(userid: str, email: str, role: str | None):
    payload = {
        "uid": userid,
        "email": email,
        "role": role,
    }
    return jwt.encode(payload, "my-secret-key", "HS256")


def validate_access_token(access_token: str):
    pass
