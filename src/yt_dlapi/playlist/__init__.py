"""Playlist API endpoint."""

from __future__ import annotations

from functools import cached_property
from typing import Any, override

from yt_dlapi.base_api_endpoint import BaseEndpoint
from yt_dlapi.playlist.models import PlaylistModel


class Playlist(BaseEndpoint[PlaylistModel]):
    """Provides methods to download, parse, and retrieve playlist data."""

    @cached_property
    @override
    def _response_model(self) -> type[PlaylistModel]:
        return PlaylistModel

    def download(self, playlist_id: str) -> dict[str, Any]:
        """Downloads playlist data for a given playlist ID.

        Args:
            playlist_id: The ID of the playlist to download.

        Returns:
            The raw JSON response as a dict, suitable for passing to ``parse()``.
        """
        url = f"https://www.youtube.com/playlist?list={playlist_id}"
        return self._client.download_yt_dlp_request(url)

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
