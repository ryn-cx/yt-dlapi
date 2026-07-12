# TODO: Validate
"""Contains the PlaylistVideos class."""

from __future__ import annotations

from typing import Any

from yt_dlapi.base_api_endpoint import BaseEndpoint
from yt_dlapi.playlist_videos.models import PlaylistVideosModel


class PlaylistVideos(BaseEndpoint[PlaylistVideosModel]):
    """Manage the playlist videos file."""

    _response_model = PlaylistVideosModel

    @staticmethod
    def has_content(response: dict[str, Any]) -> bool:
        """Return whether the playlist contains at least one video."""
        return bool(response.get("entries"))

    def download(self, playlist_id: str) -> dict[str, Any]:
        """Downloads the playlist videos file."""
        url = f"https://www.youtube.com/playlist?list={playlist_id}"
        # Need to get the episodes of the playlist so process must be True.
        return self._client.download(
            url,
            log_id=f"{self.__class__.__name__} {playlist_id}",
            process=True,
            extract_flat=True,
        )

    def get(self, playlist_id: str) -> PlaylistVideosModel:
        """Downloads and parses the playlist videos file.

        Raises:
            NoContentError: If the playlist contains no videos. The raw response
                is available on the exception's ``response`` attribute.
        """
        response = self.download(playlist_id)
        return self._parse_or_raise(
            response,
            f"{self.__class__.__name__} {playlist_id}",
        )
