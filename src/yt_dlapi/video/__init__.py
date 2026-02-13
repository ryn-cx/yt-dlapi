"""Video API endpoint."""

from __future__ import annotations

from functools import cached_property
from typing import Any, override

from yt_dlapi.base_api_endpoint import BaseEndpoint
from yt_dlapi.video.models import VideoModel


class Video(BaseEndpoint[VideoModel]):
    """Provides methods to download, parse, and retrieve video data."""

    @cached_property
    @override
    def _response_model(self) -> type[VideoModel]:
        return VideoModel

    def download(self, video_id: str) -> dict[str, Any]:
        """Downloads video data for a given video ID.

        Args:
            video_id: The ID of the video to download.

        Returns:
            The raw JSON response as a dict, suitable for passing to ``parse()``.
        """
        url = f"https://www.youtube.com/watch?v={video_id}"
        return self._client.download_yt_dlp_request(url)

    def get(self, video_id: str) -> VideoModel:
        """Downloads and parses video data for a given video ID.

        Convenience method that calls ``download()`` then ``parse()``.

        Args:
            video_id: The ID of the video to get.

        Returns:
            A Video model containing the parsed data.
        """
        data = self.download(video_id)
        return self.parse(data)
