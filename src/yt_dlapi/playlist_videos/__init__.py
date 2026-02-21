"""Playlist Videos API endpoint."""

from __future__ import annotations

from typing import Any

from yt_dlapi.base_api_endpoint import BaseEndpoint
from yt_dlapi.playlist_videos.models import PlaylistVideosModel


class PlaylistVideos(BaseEndpoint[PlaylistVideosModel]):
    """Provides methods to download, parse, and retrieve playlist videos data."""

    _response_model = PlaylistVideosModel

    def download(self, playlist_id: str) -> dict[str, Any]:
        """Downloads playlist videos data for a given playlist ID.

        Args:
            playlist_id: The ID of the playlist to download videos for.

        Returns:
            The raw JSON response as a dict, suitable for passing to ``parse()``.
        """
        url = f"https://www.youtube.com/playlist?list={playlist_id}"
        # Need to get the episodes of the playlist so process must be True.
        return self._client.download(
            url,
            process=True,
            extract_flat=True,
        )

    def get(self, playlist_id: str) -> PlaylistVideosModel:
        """Downloads and parses playlist videos data for a given playlist ID.

        Convenience method that calls ``download()`` then ``parse()``.

        Args:
            playlist_id: The ID of the playlist to get videos for.

        Returns:
            A PlaylistVideos model containing the parsed data.
        """
        response = self.download(playlist_id)
        return self.parse(response)
