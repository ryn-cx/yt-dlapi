"""Channel Playlists API endpoint."""

from __future__ import annotations

from functools import cached_property
from typing import Any, override

from yt_dlapi.base_api_endpoint import BaseEndpoint
from yt_dlapi.channel_playlists import models


class ChannelPlaylists(BaseEndpoint[models.ChannelPlaylists]):
    """Provides methods to download, parse, and retrieve channel playlists data."""

    @cached_property
    @override
    def _response_model(self) -> type[models.ChannelPlaylists]:
        """Return the Pydantic model class for this client."""
        return models.ChannelPlaylists

    def download_by_name(self, channel_name: str) -> dict[str, Any]:
        """Downloads channel playlists data for a given channel name.

        Args:
            channel_name: The name of the channel to download playlists for.

        Returns:
            The raw JSON response as a dict, suitable for passing to ``parse()``.
        """
        url = f"https://www.youtube.com/{channel_name}/playlists"
        return self._client.download_yt_dlp_request(
            url,
            process=True,
            extract_flat=True,
        )

    def download_by_id(self, channel_id: str) -> dict[str, Any]:
        """Downloads channel playlists data for a given channel ID.

        Args:
            channel_id: The ID of the channel to download playlists for.

        Returns:
            The raw JSON response as a dict, suitable for passing to ``parse()``.
        """
        url = f"https://www.youtube.com/channel/{channel_id}/playlists"
        return self._client.download_yt_dlp_request(
            url,
            process=True,
            extract_flat=True,
        )

    def get_by_name(self, channel_name: str) -> models.ChannelPlaylists:
        """Downloads and parses channel playlists data for a given channel name.

        Convenience method that calls ``download_by_name()`` then ``parse()``.

        Args:
            channel_name: The name of the channel to get playlists for.

        Returns:
            A ChannelPlaylists model containing the parsed data.
        """
        return self.parse(self.download_by_name(channel_name))

    def get_by_id(self, channel_id: str) -> models.ChannelPlaylists:
        """Downloads and parses channel playlists data for a given channel ID.

        Convenience method that calls ``download_by_id()`` then ``parse()``.

        Args:
            channel_id: The ID of the channel to get playlists for.

        Returns:
            A ChannelPlaylists model containing the parsed data.
        """
        return self.parse(self.download_by_id(channel_id))
