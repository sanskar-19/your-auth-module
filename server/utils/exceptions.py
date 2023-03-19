from fastapi import HTTPException, status


def UserAlreadyExists():
    exception = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="User Already Exists"
    )
    return exception


def InvalidToken():
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token"
    )
    return exception


def ExpiredToken():
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Expired Token"
    )
    return exception
