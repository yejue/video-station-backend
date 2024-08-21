from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination.ext.async_sqlalchemy import paginate
from fastapi_pagination import add_pagination, Page
from sqlalchemy import select


from utils import types
from database import get_db
from . import schemas, models, service


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


@router.post("/videos/{video_pid}/episodes", response_model=schemas.EpisodeOut, summary="创建分集")
async def create_episode(
        video_pid: str,
        episode: schemas.EpisodeCreate,
        db: types.AsyncSession = Depends(get_db)
):
    video = await service.VideoService.get_video_by_pid(video_pid, db)
    if not video:
        raise HTTPException(status_code=404, detail="视频不存在")

    episode = models.Episode(video_pid=video_pid, **episode.dict())
    db.add(episode)
    await db.commit()
    return episode


@router.get("/videos/{video_pid}/episodes", response_model=Page[schemas.EpisodeOut], summary="取得对应分集")
async def get_video_episodes(video_pid: str, db: types.AsyncSession = Depends(get_db)):
    stmt = select(models.Episode).where(models.Episode.video_pid == video_pid)
    episodes = await paginate(db, stmt)
    return episodes
