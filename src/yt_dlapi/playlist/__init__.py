# TODO: Validate
"""Contains the Playlist class."""

from __future__ import annotations

from typing import Any

from yt_dlapi.base_api_endpoint import BaseEndpoint
from yt_dlapi.playlist.models import PlaylistModel


class Playlist(BaseEndpoint[PlaylistModel]):
    """Manage the playlist file."""

    _response_model = PlaylistModel

    def download(self, playlist_id: str) -> dict[str, Any]:
        """Downloads the playlist file."""
        url = f"https://www.youtube.com/playlist?list={playlist_id}"
        return self._client.download(
            url,
            log_id=f"{self.__class__.__name__} {playlist_id}",
        )

    def get(self, playlist_id: str) -> PlaylistModel:
        """Downloads and parses the playlist file."""
        response = self.download(playlist_id)
        return self._parse_or_raise(
            response,
            f"{self.__class__.__name__} {playlist_id}",
        )
