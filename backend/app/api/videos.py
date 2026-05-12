from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.core.database import get_session
from app.models.user import User
from app.schemas.video import (
    VideoCreateRequest,
    VideoResponse,
    YouTubeSearchRequest,
    YouTubeVideoResult,
)
from app.services import video_service, youtube_service

router = APIRouter(prefix="/api/v1/videos", tags=["videos"])


@router.post("/search", response_model=list[YouTubeVideoResult])
async def search_videos(
    body: YouTubeSearchRequest,
    current_user: User = Depends(get_current_user),
) -> list[YouTubeVideoResult]:
    return await youtube_service.search_shorts(body.niche, body.keywords, body.max_results)


@router.post("/", response_model=VideoResponse, status_code=status.HTTP_201_CREATED)
async def create_video(
    body: VideoCreateRequest,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> VideoResponse:
    video = await video_service.create_video(session, current_user.id, body)
    return VideoResponse.model_validate(video)


@router.get("/", response_model=list[VideoResponse])
async def list_videos(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> list[VideoResponse]:
    videos = await video_service.get_videos(session, current_user.id)
    return [VideoResponse.model_validate(v) for v in videos]


@router.get("/{video_id}", response_model=VideoResponse)
async def get_video(
    video_id: UUID,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> VideoResponse:
    video = await video_service.get_video(session, current_user.id, video_id)
    return VideoResponse.model_validate(video)
