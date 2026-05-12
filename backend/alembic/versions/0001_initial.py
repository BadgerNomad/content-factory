"""initial

Revision ID: 0001
Revises:
Create Date: 2026-05-12

"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

_ts = sa.DateTime(timezone=True)
_now = sa.func.now()


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("hashed_password", sa.String(255), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", _ts, server_default=_now, nullable=False),
        sa.Column("updated_at", _ts, server_default=_now, nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)

    op.create_table(
        "videos",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("title", sa.String(500), nullable=True),
        sa.Column("original_url", sa.String(2048), nullable=True),
        sa.Column("niche", sa.String(255), nullable=True),
        sa.Column("keywords", sa.String(1000), nullable=True),
        sa.Column("status", sa.String(50), nullable=False),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("transcript", sa.Text(), nullable=True),
        sa.Column("script", sa.Text(), nullable=True),
        sa.Column("voice_url", sa.String(2048), nullable=True),
        sa.Column("video_url", sa.String(2048), nullable=True),
        sa.Column("edited_video_url", sa.String(2048), nullable=True),
        sa.Column("youtube_publish_url", sa.String(2048), nullable=True),
        sa.Column("instagram_publish_url", sa.String(2048), nullable=True),
        sa.Column("tiktok_publish_url", sa.String(2048), nullable=True),
        sa.Column("published_at", _ts, nullable=True),
        sa.Column("created_at", _ts, server_default=_now, nullable=False),
        sa.Column("updated_at", _ts, server_default=_now, nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_videos_user_id", "videos", ["user_id"])
    op.create_index("ix_videos_status", "videos", ["status"])

    op.create_table(
        "jobs",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("video_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("job_type", sa.String(50), nullable=False),
        sa.Column("status", sa.String(20), nullable=False),
        sa.Column("attempts", sa.Integer(), nullable=False),
        sa.Column("max_attempts", sa.Integer(), nullable=False),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("scheduled_at", _ts, nullable=True),
        sa.Column("started_at", _ts, nullable=True),
        sa.Column("finished_at", _ts, nullable=True),
        sa.Column("created_at", _ts, server_default=_now, nullable=False),
        sa.ForeignKeyConstraint(["video_id"], ["videos.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_jobs_video_id", "jobs", ["video_id"])
    op.create_index("ix_jobs_status", "jobs", ["status"])


def downgrade() -> None:
    op.drop_table("jobs")
    op.drop_table("videos")
    op.drop_table("users")
