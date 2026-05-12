from __future__ import annotations

import re

import httpx
from fastapi import HTTPException, status

from app.core.config import settings
from app.schemas.video import YouTubeVideoResult

_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
_VIDEOS_URL = "https://www.googleapis.com/youtube/v3/videos"
_MAX_DURATION_SECONDS = 180


def _parse_iso8601_duration(duration: str) -> int:
    match = re.fullmatch(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", duration)
    if not match:
        return 0
    hours = int(match.group(1) or 0)
    minutes = int(match.group(2) or 0)
    seconds = int(match.group(3) or 0)
    return hours * 3600 + minutes * 60 + seconds


async def search_shorts(
    niche: str, keywords: str, max_results: int = 10
) -> list[YouTubeVideoResult]:
    if not settings.YOUTUBE_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="YouTube API key not configured",
        )

    async with httpx.AsyncClient(timeout=30.0) as client:
        search_resp = await client.get(
            _SEARCH_URL,
            params={
                "part": "snippet",
                "q": f"{niche} {keywords}",
                "type": "video",
                "videoDuration": "short",
                "order": "viewCount",
                "maxResults": max_results,
                "key": settings.YOUTUBE_API_KEY,
            },
        )

        if search_resp.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"YouTube search API error: {search_resp.text}",
            )

        search_data = search_resp.json()
        items = search_data.get("items", [])

        if not items:
            return []

        video_ids = [item["id"]["videoId"] for item in items if item.get("id", {}).get("videoId")]

        if not video_ids:
            return []

        stats_resp = await client.get(
            _VIDEOS_URL,
            params={
                "part": "statistics,contentDetails",
                "id": ",".join(video_ids),
                "key": settings.YOUTUBE_API_KEY,
            },
        )

        if stats_resp.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"YouTube videos API error: {stats_resp.text}",
            )

        stats_data = stats_resp.json()
        stats_by_id: dict[str, dict] = {v["id"]: v for v in stats_data.get("items", [])}

        snippet_by_id: dict[str, dict] = {
            item["id"]["videoId"]: item["snippet"]
            for item in items
            if item.get("id", {}).get("videoId")
        }

        results: list[YouTubeVideoResult] = []
        for video_id in video_ids:
            stats_item = stats_by_id.get(video_id)
            if not stats_item:
                continue

            duration_str = stats_item.get("contentDetails", {}).get("duration", "PT0S")
            duration_seconds = _parse_iso8601_duration(duration_str)

            if duration_seconds > _MAX_DURATION_SECONDS:
                continue

            snippet = snippet_by_id.get(video_id, {})
            statistics = stats_item.get("statistics", {})

            thumbnails = snippet.get("thumbnails", {})
            thumbnail_url = (
                thumbnails.get("high", {}).get("url")
                or thumbnails.get("medium", {}).get("url")
                or thumbnails.get("default", {}).get("url")
                or ""
            )

            results.append(
                YouTubeVideoResult(
                    youtube_id=video_id,
                    title=snippet.get("title", ""),
                    channel=snippet.get("channelTitle", ""),
                    thumbnail_url=thumbnail_url,
                    view_count=int(statistics.get("viewCount", 0)),
                    duration_seconds=duration_seconds,
                    url=f"https://youtube.com/shorts/{video_id}",
                )
            )

        return results
