from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Video(Base):
    __tablename__ = "videos"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )

    title: Mapped[str | None] = mapped_column(String(500))
    original_url: Mapped[str | None] = mapped_column(String(2048))
    niche: Mapped[str | None] = mapped_column(String(255))
    keywords: Mapped[str | None] = mapped_column(String(1000))

    status: Mapped[str] = mapped_column(
        String(50), nullable=False, default="pending_transcript", index=True
    )
    error_message: Mapped[str | None] = mapped_column(Text)

    transcript: Mapped[str | None] = mapped_column(Text)
    script: Mapped[str | None] = mapped_column(Text)
    voice_url: Mapped[str | None] = mapped_column(String(2048))
    video_url: Mapped[str | None] = mapped_column(String(2048))
    edited_video_url: Mapped[str | None] = mapped_column(String(2048))

    youtube_publish_url: Mapped[str | None] = mapped_column(String(2048))
    instagram_publish_url: Mapped[str | None] = mapped_column(String(2048))
    tiktok_publish_url: Mapped[str | None] = mapped_column(String(2048))
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    user: Mapped["User"] = relationship("User", back_populates="videos")
    jobs: Mapped[list["Job"]] = relationship("Job", back_populates="video")
