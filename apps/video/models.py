import secrets

from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, Integer, String, ForeignKey
from utils.model import BaseModel


class Video(BaseModel):
    """视频基础信息表"""

    __tablename__ = 'videos'

    id = Column(Integer, primary_key=True, index=True)
    public_id = Column(String(32), unique=True, index=True, default=lambda: secrets.token_hex(16))
    title = Column(String(255), index=True, comment="视频标题")
    description = Column(String(255), comment="视频简介")
    view_count = Column(Integer, default=0, comment="播放量")
    favorite_count = Column(Integer, default=0, comment="收藏量")

    def __str__(self):
        return f"Video(id={self.id} title={self.title})"


class Episode(BaseModel):
    """视频分集信息表"""
    __tablename__ = 'episodes'

    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(Integer, ForeignKey('videos.public_id'))
    public_id = Column(String(32), unique=True, index=True, default=lambda: secrets.token_hex(16))
    title = Column(String(255), index=True, comment="分集标题")
    duration = Column(Integer, comment="分集时长（秒）")  # 时长，以秒为单位
    episode_number = Column(Integer, comment="分集序号")

    video = relationship("Video", backref=backref("episodes", cascade="all, delete-orphan"))

    def __str__(self):
        return f"Episode(id={self.id} title={self.title})"


class EpisodeLink(BaseModel):
    """分集资源表"""
    __tablename__ = 'episode_links'

    id = Column(Integer, primary_key=True, index=True)
    episode_id = Column(Integer, ForeignKey('episodes.public_id'))
    public_id = Column(String(32), unique=True, index=True, default=lambda: secrets.token_hex(16))
    url = Column(String(255))
    quality = Column(String(24))  # 质量，如 720p, 1080p
    language = Column(String(48))  # 语言，如 English, Chinese

    # 关联到分集表
    episode = relationship("Episode", backref=backref("links", cascade="all, delete-orphan"))

    def __str__(self):
        return f"EpisodeLink(id={self.id} url={self.url})"
