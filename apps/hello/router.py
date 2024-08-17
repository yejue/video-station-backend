from fastapi import APIRouter


router = APIRouter()


@router.get("/hello", summary="hello")
async def hello():
    return "hello"
