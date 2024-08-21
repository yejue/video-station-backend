from pydantic import BaseModel, Field
from typing import Optional


class VideoBase(BaseModel):
    title: str = Field(..., example="Simple Video")
    description: Optional[str] = Field(None, example="这是一个简单的视频")


class VideoCreate(VideoBase):
    pass


class VideoOut(VideoBase):
    public_id: str
    view_count: int
    favorite_count: int

    class Config:
        from_attribute = True


class EpisodeBase(BaseModel):
    title: str = Field(..., example="第一集 xxxx")
    duration: Optional[int] = Field(None, example="1234")
    episode_number: Optional[int] = Field(None, example="1")


class EpisodeCreate(EpisodeBase):
    pass


class EpisodeOut(EpisodeBase):
    public_id: str
    video_pid: str

    class Config:
        from_attribute = True


