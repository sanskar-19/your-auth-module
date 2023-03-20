from fastapi import HTTPException, status


######################### Sign Up exceptions #########################
def e_user_already_exists():
    exception = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="User Already Exists"
    )
    return exception


######################### Log In exceptions #########################
def e_invalid_credentials():
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials"
    )
    return exception

def e_user_not_found():
    exception = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Account not found"
    )

######################### Token Exceptions #########################
def e_invalid_token():
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token"
    )
    return exception


def e_expired_token():
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Expired Token"
    )
    return exception
