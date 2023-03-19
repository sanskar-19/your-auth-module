from fastapi import HTTPException, status


def getUserException():
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
    )
    return exception


def InvalidToken(message: str):
    exception = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail=str(message)
    )
    return exception
