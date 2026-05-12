from __future__ import annotations

import httpx
from fastapi import HTTPException, status

from app.core.config import settings

SUPADATA_API_URL = "https://api.supadata.ai/v1/youtube/transcript"


async def fetch_transcript(youtube_url: str) -> str:
    if not settings.SUPADATA_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Supadata API key is not configured",
        )

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            SUPADATA_API_URL,
            headers={"x-api-key": settings.SUPADATA_API_KEY},
            json={"url": youtube_url, "text": True},
        )

    if response.status_code == 404:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transcript not available",
        )

    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Supadata API error: {response.status_code} {response.text}",
        )

    data = response.json()
    transcript = data.get("content") or data.get("text") or ""
    if not transcript:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transcript not available",
        )

    return transcript
