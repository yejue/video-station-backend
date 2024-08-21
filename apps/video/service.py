from sqlalchemy import select
from utils.types import AsyncSession
from . import models


class VideoService:

    @staticmethod
    async def get_video_by_pid(pid: str, db: AsyncSession):
        stmt = select(models.Video).where(models.Video.public_id == pid)
        video = await db.scalar(stmt)
        if not video:
            return None
        return video
