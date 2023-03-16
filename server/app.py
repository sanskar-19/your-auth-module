from fastapi import FastAPI
from .routers import ums_signup

app = FastAPI()
app.include_router(ums_signup.router)
