from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, field_validator


class YouTubeSearchRequest(BaseModel):
    niche: str
    keywords: str
    max_results: int = 10

    @field_validator("max_results")
    @classmethod
    def validate_max_results(cls, v: int) -> int:
        if v < 1 or v > 50:
            raise ValueError("max_results must be between 1 and 50")
        return v


class YouTubeVideoResult(BaseModel):
    youtube_id: str
    title: str
    channel: str
    thumbnail_url: str
    view_count: int
    duration_seconds: int
    url: str


class VideoCreateRequest(BaseModel):
    youtube_id: str
    title: str
    original_url: str
    niche: str
    keywords: str


class VideoResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: UUID
    title: str | None
    original_url: str | None
    niche: str | None
    keywords: str | None
    status: str
    error_message: str | None
    created_at: datetime
    updated_at: datetime
