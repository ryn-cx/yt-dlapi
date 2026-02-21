"""Playlist API endpoint."""

from __future__ import annotations

from typing import Any

from yt_dlapi.base_api_endpoint import BaseEndpoint
from yt_dlapi.playlist.models import PlaylistModel


class Playlist(BaseEndpoint[PlaylistModel]):
    """Provides methods to download, parse, and retrieve playlist data."""

    _response_model = PlaylistModel

    def download(self, playlist_id: str) -> dict[str, Any]:
        """Downloads playlist data for a given playlist ID.

        Args:
            playlist_id: The ID of the playlist to download.

        Returns:
            The raw JSON response as a dict, suitable for passing to ``parse()``.
        """
        url = f"https://www.youtube.com/playlist?list={playlist_id}"
        return self._client.download(url)

    def get(self, playlist_id: str) -> PlaylistModel:
        """Downloads and parses playlist data for a given playlist ID.

        Convenience method that calls ``download()`` then ``parse()``.

        Args:
            playlist_id: The ID of the playlist to get.

        Returns:
            A Playlist model containing the parsed data.
        """
        response = self.download(playlist_id)
        return self.parse(response)
