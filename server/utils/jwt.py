import jwt


def create_access_token(userid: str, email: str, role: str | None):
    payload = {
        "uid": userid,
        "email": email,
        "role": role,
    }
    return jwt.encode(payload, "my-secret-key", "HS256")
