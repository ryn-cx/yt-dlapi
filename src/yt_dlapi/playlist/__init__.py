"""Playlist API endpoint."""

from __future__ import annotations

from functools import cached_property
from typing import Any, override

from yt_dlapi.base_api_endpoint import BaseEndpoint
from yt_dlapi.playlist import models


class Playlist(BaseEndpoint[models.Playlist]):
    """Provides methods to download, parse, and retrieve playlist data."""

    @cached_property
    @override
    def _response_model(self) -> type[models.Playlist]:
        """Return the Pydantic model class for this client."""
        return models.Playlist

    def download(self, playlist_id: str) -> dict[str, Any]:
        """Downloads playlist data for a given playlist ID.

        Args:
            playlist_id: The ID of the playlist to download.

        Returns:
            The raw JSON response as a dict, suitable for passing to ``parse()``.
        """
        url = f"https://www.youtube.com/playlist?list={playlist_id}"
        return self._client.download_yt_dlp_request(url)

    def parse(
        self,
        data: dict[str, Any],
        *,
        update: bool = True,
    ) -> models.Playlist:
        """Parses playlist data into a Playlist model.

        Args:
            data: The playlist data to parse.
            update: Whether to update models if parsing fails.

        Returns:
            A Playlist model containing the parsed data.
        """
        if update:
            return self._parse_response(data)

        return models.Playlist.model_validate(data)

    def get(self, playlist_id: str) -> models.Playlist:
        """Downloads and parses playlist data for a given playlist ID.

        Convenience method that calls ``download()`` then ``parse()``.

        Args:
            playlist_id: The ID of the playlist to get.

        Returns:
            A Playlist model containing the parsed data.
        """
        response = self.download(playlist_id)
        return self.parse(response)
