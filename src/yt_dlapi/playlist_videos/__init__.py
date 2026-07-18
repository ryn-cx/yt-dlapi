# TODO: Validate
"""Contains the PlaylistVideos class."""

from __future__ import annotations

from logging import NullHandler, getLogger
from typing import Any

from yt_dlapi.base_api_endpoint import BaseEndpoint
from yt_dlapi.playlist_videos.models import PlaylistVideosModel

logger = getLogger(__name__)
logger.addHandler(NullHandler())


class PlaylistVideos(BaseEndpoint[PlaylistVideosModel]):
    """Manage the playlist videos file."""

    _response_model = PlaylistVideosModel

    @staticmethod
    def has_content(response: dict[str, Any]) -> bool:
        """Return whether the playlist contains at least one video."""
        return bool(response.get("entries"))

    def get_log_id(self, playlist_id: str) -> str:
        """Build the log id for a download."""
        return f"{self.__class__.__name__} {playlist_id=}"

    def download(self, playlist_id: str) -> dict[str, Any]:
        """Downloads the playlist videos file."""
        url = f"https://www.youtube.com/playlist?list={playlist_id}"
        # Need to get the episodes of the playlist so process must be True.
        return self._client.download(
            url,
            log_id=self.get_log_id(playlist_id),
            process=True,
            extract_flat=True,
        )

    def download_and_parse(self, playlist_id: str) -> PlaylistVideosModel:
        """Downloads and parses the playlist videos file.

        Raises:
            NoContentError: If the playlist contains no videos. The raw response
                is available on the exception's ``response`` attribute.
        """
        return self._parse_or_raise(
            self.download(playlist_id),
            self.get_log_id(playlist_id),
        )
