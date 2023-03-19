from fastapi import HTTPException, status


def getUserException():
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
    )
    return exception


def InvalidToken():
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail=str("Invalid Token")
    )
    return exception


def ExpiredToken():
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail=str("Expired Token")
    )
    return exception
