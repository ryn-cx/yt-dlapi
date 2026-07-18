# TODO: Validate
"""Contains the Video class."""

from __future__ import annotations

from logging import NullHandler, getLogger
from typing import Any

from yt_dlapi.base_api_endpoint import BaseEndpoint
from yt_dlapi.video.models import VideoModel

logger = getLogger(__name__)
logger.addHandler(NullHandler())


class Video(BaseEndpoint[VideoModel]):
    """Manage the video file."""

    _response_model = VideoModel

    def get_log_id(self, video_id: str) -> str:
        """Build the log id for a download."""
        return f"{self.__class__.__name__} {video_id=}"

    def download(self, video_id: str) -> dict[str, Any]:
        """Downloads the video file."""
        url = f"https://www.youtube.com/watch?v={video_id}"
        return self._client.download(
            url,
            log_id=self.get_log_id(video_id),
        )

    def download_and_parse(self, video_id: str) -> VideoModel:
        """Downloads and parses the video file."""
        return self.parse(self.download(video_id))
