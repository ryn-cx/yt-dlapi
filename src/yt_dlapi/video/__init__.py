# TODO: Validate
"""Contains the Video class."""

from __future__ import annotations

from typing import Any

from yt_dlapi.base_api_endpoint import BaseEndpoint
from yt_dlapi.video.models import VideoModel


class Video(BaseEndpoint[VideoModel]):
    """Manage the video file."""

    _response_model = VideoModel

    def download(self, video_id: str) -> dict[str, Any]:
        """Downloads the video file."""
        url = f"https://www.youtube.com/watch?v={video_id}"
        return self._client.download(
            url,
            log_id=f"{self.__class__.__name__} {video_id}",
        )

    def get(self, video_id: str) -> VideoModel:
        """Downloads and parses the video file."""
        data = self.download(video_id)
        return self._parse_or_raise(data, f"{self.__class__.__name__} {video_id}")
