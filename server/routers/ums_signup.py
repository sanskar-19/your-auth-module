from fastapi import APIRouter

router = APIRouter(prefix="/api/signup")


@router.post("/")
async def root():
    return {"response": "response"}
