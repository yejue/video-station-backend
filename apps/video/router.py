from fastapi import APIRouter, Depends
from fastapi_pagination.ext.async_sqlalchemy import paginate
from fastapi_pagination import add_pagination, Page
from sqlalchemy import select


from utils import types
from database import get_db
from . import schemas, models


router = APIRouter()
add_pagination(router)


@router.post("/videos", response_model=schemas.VideoOut, summary="创建视频集")
async def create_video(video: schemas.VideoCreate, db: types.AsyncSession = Depends(get_db)):
    new_video = models.Video(**video.dict())
    db.add(new_video)
    await db.commit()
    return new_video


@router.get("/videos", response_model=Page[schemas.VideoOut], summary="取得视频集")
async def get_videos(db: types.AsyncSession = Depends(get_db)):
    return await paginate(db, select(models.Video))

