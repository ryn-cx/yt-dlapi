"""Channel API endpoint."""

from __future__ import annotations

from functools import cached_property
from typing import Any, override

from yt_dlapi.base_api_endpoint import BaseEndpoint
from yt_dlapi.channel.models import ChannelModel


class Channel(BaseEndpoint[ChannelModel]):
    """Provides methods to download, parse, and retrieve channel data."""

    @cached_property
    @override
    def _response_model(self) -> type[ChannelModel]:
        """Return the Pydantic model class for this client."""
        return ChannelModel

    def download_by_name(self, channel_name: str) -> dict[str, Any]:
        """Downloads channel data for a given channel name.

        Args:
            channel_name: The name of the channel to download.

        Returns:
            The raw JSON response as a dict, suitable for passing to ``parse()``.
        """
        url = f"https://www.youtube.com/@{channel_name}"
        return self._client.download_yt_dlp_request(url)

    def download_by_id(self, channel_id: str) -> dict[str, Any]:
        """Downloads channel data for a given channel ID.

        Args:
            channel_id: The ID of the channel to download.

        Returns:
            The raw JSON response as a dict, suitable for passing to ``parse()``.
        """
        url = f"https://www.youtube.com/channel/{channel_id}"
        return self._client.download_yt_dlp_request(url)

    def get_by_name(self, channel_name: str) -> ChannelModel:
        """Downloads and parses channel data for a given channel name.

        Convenience method that calls ``download_by_name()`` then ``parse()``.

        Args:
            channel_name: The name of the channel to get.

        Returns:
            A Channel model containing the parsed data.
        """
        return self.parse(self.download_by_name(channel_name))

    def get_by_id(self, channel_id: str) -> ChannelModel:
        """Downloads and parses channel data for a given channel ID.

        Convenience method that calls ``download_by_id()`` then ``parse()``.

        Args:
            channel_id: The ID of the channel to get.

        Returns:
            A Channel model containing the parsed data.
        """
        return self.parse(self.download_by_id(channel_id))
