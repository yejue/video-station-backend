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


@router.get(
    "/videos/{video_pid}/episodes",
    response_model=Page[schemas.EpisodeOutWithLinks],
    summary="取得对应分集"
)
async def get_video_episodes(video_pid: str, db: types.AsyncSession = Depends(get_db)):
    stmt = select(models.Episode).where(models.Episode.video_pid == video_pid)
    episodes = await paginate(db, stmt)
    return episodes


@router.post(
    "/videos/{episode_pid}/episode-links",
    response_model=schemas.EpisodeLinkOut,
    summary="创建分集资源"
)
async def create_episode_link(
        episode_pid: str,
        episode_link: schemas.EpisodeLinkCreate,
        db: types.AsyncSession = Depends(get_db)
):
    episode = await service.VideoService.get_episode_by_pid(episode_pid, db)
    if not episode:
        raise HTTPException(status_code=404, detail="对应剧集不存在")
    episode_link = models.EpisodeLink(episode=episode, **episode_link.dict())
    db.add(episode_link)
    await db.commit()
    return episode_link


@router.get(
    "/videos/{episode_pid}/episode-links",
    response_model=Page[schemas.EpisodeLinkOut],
    summary="取得分集资源"
)
async def get_episode_links(episode_pid: str, db: types.AsyncSession = Depends(get_db)):
    stmt = select(models.EpisodeLink).where(models.EpisodeLink.episode_pid == episode_pid)
    return await paginate(db, stmt)
