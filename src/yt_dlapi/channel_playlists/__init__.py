"""Channel Playlists API endpoint."""

from __future__ import annotations

from typing import Any

from yt_dlapi.base_api_endpoint import BaseEndpoint
from yt_dlapi.channel_playlists.models import ChannelPlaylistsModel


class ChannelPlaylists(BaseEndpoint[ChannelPlaylistsModel]):
    """Provides methods to download, parse, and retrieve channel playlists data."""

    _response_model = ChannelPlaylistsModel

    def download_by_name(self, channel_name: str) -> dict[str, Any]:
        """Downloads channel playlists data for a given channel name.

        Args:
            channel_name: The name of the channel to download playlists for.

        Returns:
            The raw JSON response as a dict, suitable for passing to ``parse()``.
        """
        url = f"https://www.youtube.com/{channel_name}/playlists"
        return self._client.download(
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
        return self._client.download(
            url,
            process=True,
            extract_flat=True,
        )

    def get_by_name(self, channel_name: str) -> ChannelPlaylistsModel:
        """Downloads and parses channel playlists data for a given channel name.

        Convenience method that calls ``download_by_name()`` then ``parse()``.

        Args:
            channel_name: The name of the channel to get playlists for.

        Returns:
            A ChannelPlaylists model containing the parsed data.
        """
        return self.parse(self.download_by_name(channel_name))

    def get_by_id(self, channel_id: str) -> ChannelPlaylistsModel:
        """Downloads and parses channel playlists data for a given channel ID.

        Convenience method that calls ``download_by_id()`` then ``parse()``.

        Args:
            channel_id: The ID of the channel to get playlists for.

        Returns:
            A ChannelPlaylists model containing the parsed data.
        """
        return self.parse(self.download_by_id(channel_id))
