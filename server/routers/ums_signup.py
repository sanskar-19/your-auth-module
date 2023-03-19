from fastapi import APIRouter, Header, HTTPException, status
import jwt
from ..models import user
from ..utils import exceptions, user as Utiluser
from typing import Union
import os
import uuid




router = APIRouter(prefix="/api/ums")


#test get function
@router.get("/items/{item_id}")
async def read_root(item_id: int, q: Union[str,None]=None):
    return {"item id":item_id,"q":q}

#test put request
@router.put("/items/{item_id}")
async def put1(item_id:int, user: user.NewUserModel):
    return user
    
# signup
@router.post("/signup")
async def signup(user: user.NewUserModel):

    
    key,encoded_user_password = Utiluser.encode_password(user.password) # this key and encoded password will be stored in DB
    return key,encoded_user_password



# login
@router.post("/signin")
async def signin(user: user.ExistingUserModel):

    
    key,encoded_user_password = Utiluser.encode_password("hello123") # this key and encoded password will be there in the DB
   
    if Utiluser.password_matcher(key, encoded_user_password, user.password):

        print("Login Successful")
        user_id=str(uuid.uuid1())

        payload_data = {
        "session_id":user_id,
        "email": user.email
        }       

        token=jwt.encode(payload=payload_data,key=os.getenv("mysecret"))  
        return token

    else:
        print("incorrect password")

   

# tokentest
@router.post("/test", status_code=status.HTTP_201_CREATED)
async def token(token: str | None = Header(default=None)):
    if not token:
        raise exceptions.getUserException()
    return token
