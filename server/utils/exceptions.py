from fastapi import HTTPException, status


def getUserException():
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
    )
    return exception
