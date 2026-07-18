# TODO: Validate
"""Contains the Playlist class."""

from __future__ import annotations

from logging import NullHandler, getLogger
from typing import Any

from yt_dlapi.base_api_endpoint import BaseEndpoint
from yt_dlapi.playlist.models import PlaylistModel

logger = getLogger(__name__)
logger.addHandler(NullHandler())


class Playlist(BaseEndpoint[PlaylistModel]):
    """Manage the playlist file."""

    _response_model = PlaylistModel

    def get_log_id(self, playlist_id: str) -> str:
        """Build the log id for a download."""
        return f"{self.__class__.__name__} {playlist_id=}"

    def download(self, playlist_id: str) -> dict[str, Any]:
        """Downloads the playlist file."""
        url = f"https://www.youtube.com/playlist?list={playlist_id}"
        return self._client.download(
            url,
            log_id=self.get_log_id(playlist_id),
        )

    def download_and_parse(self, playlist_id: str) -> PlaylistModel:
        """Downloads and parses the playlist file."""
        return self.parse(self.download(playlist_id))
