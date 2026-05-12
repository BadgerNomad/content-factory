from __future__ import annotations

from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.video import Video
from app.schemas.video import VideoCreateRequest


async def create_video(session: AsyncSession, user_id: UUID, data: VideoCreateRequest) -> Video:
    video = Video(
        user_id=user_id,
        title=data.title,
        original_url=data.original_url,
        niche=data.niche,
        keywords=data.keywords,
        status="pending_transcript",
    )
    session.add(video)
    await session.commit()
    await session.refresh(video)
    return video


async def get_videos(session: AsyncSession, user_id: UUID) -> list[Video]:
    result = await session.execute(select(Video).where(Video.user_id == user_id))
    return list(result.scalars().all())


async def get_video(session: AsyncSession, user_id: UUID, video_id: UUID) -> Video:
    video = await session.get(Video, video_id)
    if video is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Video not found")
    if video.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    return video
