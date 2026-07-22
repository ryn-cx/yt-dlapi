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

    def download(self, video_id: str) -> dict[str, Any]:
        """Downloads the video file."""
        log_id = self.get_log_id(self.download, locals())
        url = f"https://www.youtube.com/watch?v={video_id}"
        return self._client.download(
            url,
            log_id=log_id,
        )

    def download_and_parse(self, video_id: str) -> VideoModel:
        """Downloads and parses the video file."""
        return self.parse(self.download(video_id))
