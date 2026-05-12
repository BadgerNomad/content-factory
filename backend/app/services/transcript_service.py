from __future__ import annotations

from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.video import Video
from app.services import supadata_service


async def process_transcript(session: AsyncSession, video_id: UUID, user_id: UUID) -> Video:
    video = await session.get(Video, video_id)
    if video is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Video not found")
    if video.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    if video.status != "pending_transcript":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Video is not in pending_transcript status (current: {video.status})",
        )

    try:
        transcript = await supadata_service.fetch_transcript(video.original_url)
        video.transcript = transcript
        video.status = "pending_script"
        video.error_message = None
    except Exception as exc:
        video.status = "error_transcript"
        video.error_message = str(exc)
        await session.commit()
        raise

    await session.commit()
    await session.refresh(video)
    return video
